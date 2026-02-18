import subprocess
import time

def test_cli_workflow():
    start_time = time.time()
    
    # Run the CLI command
    command = ["python3", "main.py", "cli", "--query", "Quel est le meilleur moment pour planter le maïs ?", "--region", "Centre"]
    
    print(f"Running command: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=60)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print("\n--- Result ---")
        if result.returncode == 0:
            print("Workflow executed successfully.")
            print(f"Output length: {len(result.stdout)} characters")
            print("Output snippet:")
            print(result.stdout[:1000] + "..." if len(result.stdout) > 1000 else result.stdout)
        else:
            print("Workflow failed.")
            print("Error output:")
            print(result.stderr)
            print("Standard output:")
            print(result.stdout)
            
        print(f"\n--- Performance ---")
        print(f"Total execution time: {elapsed_time:.2f} seconds")
        
    except subprocess.TimeoutExpired:
        print("Workflow timed out after 60 seconds.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_cli_workflow()
