import zipfile
import io

def repair_and_read():
    file_path = 'Sony FE Lens.xlsx'
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Try to find the central directory manually or just open as is
        try:
            zf = zipfile.ZipFile(io.BytesIO(data))
            print("Files in zip:", zf.namelist())
        except Exception as e:
            print(f"Standard zip open failed: {e}")
            # If standard fails, we might need a more complex repair
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    repair_and_read()
