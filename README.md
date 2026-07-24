# Insurance Support Ticket Triage Agent

## 1. Step-by-step setup instructions

1. Clone or download the project repository.

2. Open the project directory in your Python IDE.

3. Create a Python 3.11 Conda environment:

```bash
conda create -n hdi-ticket-triage python=3.11
```

4. Activate the environment:

```bash
conda activate hdi-ticket-triage
```

5. Install the required Python packages:

```bash
pip install -r requirements.txt
```

6. Install Ollama locally and verify the installation:

```bash
ollama --version
```

7. Download the configured local language model:

```bash
ollama pull qwen3:1.7b
```

8. Confirm that the model is available:

```bash
ollama list
```

## 2. Dependencies and environment setup

The prototype was developed with:

- Python 3.11
- pandas
- LangChain
- langchain-ollama
- Pydantic
- Ollama
- Qwen3 1.7B
- tqdm
- pytest
- Jupyter Notebook

The project uses a local Conda environment named:

```text
hdi-ticket-triage
```

All model inference is performed locally through Ollama. No paid API or cloud-based language model is required.

## 3. Downloading the dataset from Kaggle

The project uses the public Kaggle dataset:

**Customer IT Support – Ticket Dataset**

Download the dataset from Kaggle and place the CSV file in the following directory:

```text
data/
```

The expected file structure is:

```text
data/
└── dataset_tickets.csv
```

If the downloaded file has a different name, update the input path in `main.py`:

```python
INPUT_PATH = Path("data/dataset_tickets.csv")
```

The application uses the following columns as model input:

- `subject`
- `body`

The following existing columns are intentionally excluded from the model input to avoid information leakage:

- `answer`
- `type`
- `queue`
- `priority`
- `tag_1` to `tag_8`

## 4. Running the code on a sample batch

Ensure that Ollama is running and that `qwen3:1.7b` has been downloaded.

To run a small sample:

```bash
python run_sample.py
```

To run the configured batch:

```bash
python main.py
```

The batch size can be changed in `main.py`:

```python
SAMPLE_SIZE = 200
```

The generated result file is written to:

```text
outputs/triage_results.csv
```

The output includes:

- ticket ID
- original subject and body
- predicted topic
- predicted urgency
- information assessment
- missing information
- clarification question
- recommended next action
- classification notes
- processing status
- processing time

## 5. Environment variables and configuration

No environment variables are required for the current local prototype.

The language model configuration is stored in:

```text
src/config.py
```

Current configuration:

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    model_name: str = "qwen3:1.7b"
    temperature: float = 0.0


settings = Settings()
```

To use another locally installed Ollama model, change `model_name`:

```python
model_name: str = "qwen3:4b"
```

The input file, output file and batch size are configured in `main.py`:

```python
INPUT_PATH = Path("data/dataset_tickets.csv")
OUTPUT_PATH = Path("outputs/triage_results.csv")
SAMPLE_SIZE = 200
```