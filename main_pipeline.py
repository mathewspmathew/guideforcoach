from src.config import RAW_DATA_PATH
from src.preprocess import DataPreprocessor
from src.model import SimilarityEngine

def run_pipeline():
    print("--- Starting Moneyball Pipeline ---")

    # Step 1: Data Engineering
    print("\n[Step 1] Loading and Cleaning Data...")
    processor = DataPreprocessor(RAW_DATA_PATH)
    df_clean = processor.load_clean_data()

    # Step 2: Model Training
    print("\n[Step 2] Training AI Model...")
    engine = SimilarityEngine()
    engine.train(df_clean)

    # Step 3: Test Inference (Sanity Check)
    print("\n[Step 3] Testing Inference...")
    test_player = "Haaland"  # Change this to test
    result = engine.inference(test_player)

    print(f"\n🔎 Query: {test_player}")
    if "error" in result:
        print(f"❌ {result['error']}")
    else:
        print(f"✅ Found match for: {result['target']} ({result['target_squad']})")
        print("   Top Recommendations:")
        for p in result['recommendations']:
            print(f"   - {p['name']} ({p['squad']}) [Sim: {p['similarity']}%]")

if __name__ == "__main__":
    run_pipeline()