# AiApiHomeAssignment
Async Python application that analyzes Git repositories using OpenAI's APIs
Installation Guide:

    Prerequisites:

    - Python 3.10+ (Ensure that Python is installed on your system)

    - Git (Ensure that Git is installed on your system)

    - OpenAI API Key (You can get your API key from OpenAI)

    - docker descktop (optional)
    
    Setup:

    - Clone this repository:

        git clone <repository_url>
        cd <repository_directory>

    - Set up a virtual environment:

        python3 -m venv venv
        source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

    - Install dependencies:

        pip install -r requirements.txt

    - create .env file in config with your OpenAi key and pinecone key :

        OPENAI_API_KEY = "your_api_key"
        PINECONE_API_KEY = "your_api_key"

    - Ensure that Git is installed and configured on your system.

    docker build -t repository_analyzer .
docker run -p 8000:8000 repository_analyzer


Usage Examples:

    - Running main.py file

    - Running with docker:

        docker build -t repository_analyzer .
        docker run -p 8000:8000 repository_analyzer

    - Running with cli:

        python src/cli.py analyze-repo --repo-url https://github.com/example/repo.git



Design Decisions:

    - Asynchronous Architecture: The application was designed to be asynchronous using asyncio to allow multiple operations (such as fetching data from multiple repositories or analyzing large amounts of code) to run concurrently without blocking.

    - Git Integration: GitPython is used to interact with Git repositories. This allows for seamless integration to clone, fetch, and pull code from remote repositories.

    - Vector Database: OpenAI's Vector Database (or alternative like Pinecone) is used for storing code vectors. These vectors are generated using the OpenAI Embeddings API, enabling efficient and fast search and analysis of code.

    - Assistants API: The OpenAI Assistants API is used for intelligent code analysis, which includes explanations of the code, error detection, and potential improvements.

    - Information Security: Store API keys in a .env file to keep them private.


Performance Considerations:

    - Rate Limiting: Since OpenAI's APIs may have rate limits, the application uses async features to handle multiple requests concurrently but avoids overwhelming the API with too many simultaneous calls.

    - Efficient Vector Storage: Using a vector database ensures that the code's semantic representation is stored efficiently, allowing for fast similarity searches and analysis. However, depending on the repository size, memory and database storage should be considered.

    - Large Repositories: For very large codebases, you might want to limit the number of files or lines analyzed at once, or batch the requests to avoid high memory consumption and time delays.

    - Error Handling: The application includes error handling for network failures, API limits, and other potential issues during the analysis process.


Future Improvements

    - Support for Additional File Types: Expand the application to analyze more types of files.

    - Improved Testing: Enhance test coverage and quality to ensure reliability.

    - Batch Analysis: Implement functionality to analyze multiple repositories or large codebases in batches to improve scalability.

    - Enhanced Code Summarization: Improve the intelligence of the code analysis by incorporating additional machine learning models or custom fine-tuned versions of the OpenAI models.

    - Performance Optimizations: Optimize the storage and retrieval of code vectors by exploring advanced techniques such as vector quantization or hybrid databases.

    - User Interface: Add a web-based user interface (UI) for easier interaction with the application, allowing users to visualize code analysis results and explore repositories interactively.

    - Advanced Repository Insights: Implement more advanced analysis features, such as detecting design patterns, code smells, and refactoring suggestions.

    - CI/CD Integration: Integrate with popular CI/CD tools for automatic analysis on new commits or pull requests, ensuring ongoing code quality.

    - Version Management: Managed through Jenkins pipeline.
    
    - Add api key encryption








     