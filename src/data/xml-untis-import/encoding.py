import chardet

file_path = 'untis.xml'
with open(file_path, 'rb') as f:
    raw_data = f.read()
    result = chardet.detect(raw_data)
    print(f"Detected encoding: {result['encoding']}, Confidence: {result['confidence']}")