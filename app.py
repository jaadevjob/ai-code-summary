import os
import logging
import shutil
import glob
import markdown
from git import Repo
from urllib.parse import urlparse

from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import jsonschema
from jsonschema import validate

from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_community.document_loaders.directory import DirectoryLoader
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
import datetime

app = Flask(__name__)
load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

llm = AzureChatOpenAI(
    azure_deployment=os.getenv('AZURE_OPENAI_DEPLOYMENT'),
    temperature=0,
    model_kwargs={
        "top_p": 0.9
    },
    verbose=True,
    azure_endpoint=os.getenv('AZURE_OPENAI_API_BASE')
)

# Create repos directory (local) if it doesn't exist
try:
    repos_path = "./repos"
    os.makedirs(repos_path, exist_ok=True)
    logger.debug("Repos directory created.")
except Exception as e:
    logger.debug(f"Error creating repos directory: {str(e)}")

# Get repo name from URL
def get_repo_name_from_url(url):
    path = urlparse(url).path
    return path.split('/')[-1]

# Load prompt from file
def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Code summary API endpoint Route
@app.route('/api/codesum', methods=['POST'])
def api():
    schema = {
        "type": "object",
        "properties": {
            "path": {"type": "string"}
        },
        "required": ["path"]
    }
    
    data = request.get_json()
    logger.debug(f"Request data: {data}")
    
    try:
        validate(instance=data, schema=schema)
    except jsonschema.exceptions.ValidationError as e:
        return jsonify({"error": str(e)}), 400

    repo_url = data.get('path')
    repo_name = get_repo_name_from_url(repo_url)
    repo_path = os.path.join(repos_path, repo_name)

    # Check if repo exists and is older than 24 hours
    if os.path.exists(repo_path):
        creation_time = datetime.datetime.fromtimestamp(os.path.getctime(repo_path))
        current_time = datetime.datetime.now()
        time_difference = current_time - creation_time
        if time_difference.total_seconds() > 24 * 60 * 60:
            shutil.rmtree(repo_path)

    # Clone the repo if it doesn't exist or was deleted
    if not os.path.exists(repo_path):
        try:
            repo = Repo.clone_from(repo_url, to_path=repo_path)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        repo = Repo(repo_path)

    commit_message = repo.head.commit.message
    commit_author = str(repo.head.commit.author)

    # Load documents w/ Directory Loader
    loader = DirectoryLoader(
        repo_path,
        glob="**/*",
        loader_cls=TextLoader,
        exclude=[
            "**/non-utf8-encoding.py",
            "*.ico",
            "*.pdf",
            "*.pptx",
            "*.docx",
            "*.xlsx",
            "*.png",
            "*.jpg",
        ]
    )
    documents = loader.load()

    # Text Splitter
    python_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=200
    )
    texts = python_splitter.split_documents(documents)

    # Text embeddings
    db = Chroma.from_documents(texts, 
            AzureOpenAIEmbeddings(
                disallowed_special=(),
                azure_endpoint=os.getenv('AZURE_OPENAI_API_BASE'),
                retry_min_seconds=5,
                max_retries=5
            )
        )

    num_elements_in_index = len(texts)
    num_results_requested = 20  # Or any number you want to request
    num_results = min(num_results_requested, num_elements_in_index)

    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": num_results},
    )

    search_prompt = ChatPromptTemplate.from_messages(
        [
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
            (
                "user",
                "Given the above conversation, generate a search query to look up to get information relevant to the conversation",
            ),
        ]
    )

    retriever_chain = create_history_aware_retriever(llm, retriever, search_prompt)

    response_prompt_text = load_prompt('./prompts/codesum_prompt.txt')
    response_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                response_prompt_text
            ),
            ("placeholder", "{chat_history}"),
            ("user", "{input}"),
        ]
    )
    document_chain = create_stuff_documents_chain(llm, response_prompt)

    qa = create_retrieval_chain(retriever_chain, document_chain)

    result = qa.invoke(
        {
            "input": "",
            "context": "Example context",
            "commit_message": commit_message,
            "commit_author": commit_author
        }
    )  # Empty input since the question is in the prompt

    response_json = {
        "commit_message": commit_message,
        "commit_author": commit_author,
        "summary": result["answer"]
    }

    
    return jsonify(response_json)

@app.route('/api/translate', methods=['POST'])
def translate():

    schema = {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "language": {"type": "string"}
        },
        "required": ["text", "language"]
    }

    data = request.get_json()
    text = data.get('text')
    language = data.get('language')

    logger.debug(f"Translate request to: {language}")

    response = llm.invoke(
        f"Translate the following text to {language}:\n{text}\nDon't translate the code blocks."
    )
    logger.debug(f"Response: {response}")
    response_json = jsonify({
        "translatedText": response.content
    })

    logger.debug(f"Response JSON: {response_json}")

    return response_json

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
