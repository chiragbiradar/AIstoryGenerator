import os
from openai import OpenAI
import json

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = ''  # Replace with your OpenAI API key
client = OpenAI()

# Step 1: Prepare the Dataset
def prepare_dataset():
    # Example dataset (replace with your actual dataset)
    data = [
        {
            "messages": [
                {"role": "system", "content": "You are a creative storyteller."},
                {"role": "user", "content": "Write a story about a brave knight."},
                {"role": "assistant", "content": "Once upon a time, a brave knight named Sir Alistair set out on a quest to save his kingdom from a fearsome dragon..."}
            ]
        },
        {
            "messages": [
                {"role": "system", "content": "You are a creative storyteller."},
                {"role": "user", "content": "Write a story about a time-traveling scientist."},
                {"role": "assistant", "content": "Dr. Emily Carter had always been fascinated by the concept of time. One day, she invented a machine that could transport her to any era..."}
            ]
        }
        # Add more examples
    ]

    # Save the dataset as a JSONL file
    with open("D:/storyGeneratorAi/f54c09fd23315a6f9c86f9dc80f725de7d8f9c64/dataset_info.json", "w") as f:
        for entry in data:
            f.write(json.dumps(entry) + "\n")

    print("Dataset prepared and saved as 'D:/storyGeneratorAi/f54c09fd23315a6f9c86f9dc80f725de7d8f9c64/dataset_info.json'.")

# Step 2: Upload the Dataset
def upload_dataset():
    # Upload the dataset to OpenAI
    response = client.files.create(
        file=open("D:/storyGeneratorAi/f54c09fd23315a6f9c86f9dc80f725de7d8f9c64/dataset_info.json", "rb"),
        purpose="fine-tune"
    )
    file_id = response.id
    print(f"Dataset uploaded. File ID: {file_id}")
    return file_id

# Step 3: Start the Fine-Tuning Job
def start_fine_tuning(file_id):
    # Start the fine-tuning job
    response = client.fine_tuning.jobs.create(
        training_file=file_id,
        model="gpt-3.5-turbo",  # Use GPT-3.5 Turbo
        hyperparameters={
            "n_epochs": 3,  # Number of epochs
            "batch_size": 4,  # Batch size
            "learning_rate_multiplier": 0.1  # Learning rate
        }
    )
    job_id = response.id
    print(f"Fine-tuning job started. Job ID: {job_id}")
    return job_id

# Step 4: Monitor the Fine-Tuning Job
def monitor_fine_tuning(job_id):
    # Retrieve the status of the fine-tuning job
    job = client.fine_tuning.jobs.retrieve(job_id)
    print(f"Job Status: {job.status}")
    return job.status

# Step 5: Test the Fine-Tuned Model
def test_fine_tuned_model(model_id):
    # Generate a story using the fine-tuned model
    completion = client.chat.completions.create(
        model=model_id,  # Use your fine-tuned model ID
        messages=[
            {"role": "system", "content": "You are a creative storyteller."},
            {"role": "user", "content": "Write a story about a magical forest."}
        ]
    )
    print("Generated Story:")
    print(completion.choices[0].message.content)

# Step 6: Use GPT-4 with Prompt Engineering
def use_gpt4_with_prompt_engineering():
    # System prompt to guide GPT-4
    system_prompt = """
    You are a creative storyteller. Your task is to generate engaging, coherent, and imaginative stories based on user inputs. Follow these guidelines:
    1. Develop a clear plot with a beginning, middle, and end.
    2. Create well-defined characters with unique traits.
    3. Use vivid descriptions to bring the story to life.
    4. Ensure the story is appropriate for all audiences.
    """

    # Few-shot examples
    examples = [
        {
            "role": "user",
            "content": "Write a story about a brave knight and a dragon."
        },
        {
            "role": "assistant",
            "content": "Once upon a time, in a land far away, a brave knight named Sir Alistair faced a fearsome dragon..."
        }
    ]

    # Generate a story using GPT-4
    completion = client.chat.completions.create(
        model="gpt-4",  # Use GPT-4
        messages=[
            {"role": "system", "content": system_prompt},
            *examples,  # Include few-shot examples
            {"role": "user", "content": "Write a story about a time-traveling scientist."}
        ]
    )
    print("Generated Story (GPT-4):")
    print(completion.choices[0].message.content)

# Main Workflow
def main():
    # Step 1: Prepare the dataset
    prepare_dataset()

    # Step 2: Upload the dataset
    file_id = upload_dataset()

    # Step 3: Start the fine-tuning job
    job_id = start_fine_tuning(file_id)

    # Step 4: Monitor the fine-tuning job
    status = monitor_fine_tuning(job_id)
    if status == "succeeded":
        # Step 5: Test the fine-tuned model
        model_id = f"ft:gpt-3.5-turbo:your-model-id"  # Replace with your fine-tuned model ID
        test_fine_tuned_model(model_id)

    # Step 6: Use GPT-4 with prompt engineering
    use_gpt4_with_prompt_engineering()

if __name__ == "__main__":
    main()