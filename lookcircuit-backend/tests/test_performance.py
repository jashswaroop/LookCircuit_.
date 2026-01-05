"""
Performance Benchmarks for LookCircuit
Tests latency and throughput requirements.
"""

import time
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


def benchmark(func, iterations=10, warmup=2):
    """Run a function multiple times and return timing statistics."""
    # Warmup runs
    for _ in range(warmup):
        func()
    
    # Timed runs
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        elapsed = (time.perf_counter() - start) * 1000  # ms
        times.append(elapsed)
    
    return {
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'min': min(times),
        'max': max(times),
        'stdev': statistics.stdev(times) if len(times) > 1 else 0
    }


def test_skin_tone_latency():
    """Benchmark skin tone detection latency."""
    import cv2
    import numpy as np
    from ai.face_analysis.skin_tone import SkinToneDetector
    
    detector = SkinToneDetector()
    
    # Create test image
    lab = np.zeros((100, 100, 3), dtype=np.float32)
    lab[:, :, 0] = 60 * 255 / 100
    lab[:, :, 1] = 144
    lab[:, :, 2] = 146
    test_img = cv2.cvtColor(lab.astype(np.uint8), cv2.COLOR_LAB2BGR)
    
    def run():
        detector.analyze([test_img])
    
    return benchmark(run)


def test_face_shape_latency():
    """Benchmark face shape classification latency."""
    from ai.face_analysis.face_shape import FaceShapeClassifier
    
    classifier = FaceShapeClassifier()
    measurements = {
        'length_width_ratio': 1.2,
        'forehead_jaw_ratio': 1.0,
        'jawline_angle': 140,
        'forehead_width': 100,
        'jaw_width': 100,
        'cheekbone_width': 95
    }
    
    def run():
        classifier.classify(measurements)
    
    return benchmark(run)


def test_recommendation_engine_latency():
    """Benchmark recommendation generation latency."""
    from ai.recommendation_engine.color_theory import RecommendationEngine
    
    engine = RecommendationEngine()
    
    def run():
        engine.generate_recommendations(
            fitzpatrick_type=3,
            undertone="warm",
            face_shape="oval",
            body_type="mesomorph",
            hair_coverage="full",
            gender="male"
        )
    
    return benchmark(run)


def test_product_discovery_latency():
    """Benchmark product discovery latency."""
    from ai.product_discovery.scraper import ProductDiscoveryEngine
    
    engine = ProductDiscoveryEngine()
    
    def run():
        engine.discover_products(
            color_palette=["#000080", "#FFFFFF"],
            categories=["shirts", "footwear", "eyewear"]
        )
    
    return benchmark(run)


def run_all_benchmarks():
    """Run all benchmarks and report results."""
    print("=" * 70)
    print("LOOKCIRCUIT PERFORMANCE BENCHMARKS")
    print("=" * 70)
    
    # Target: <500ms for API response, <3000ms for full analysis
    benchmarks = [
        ("Skin Tone Detection", test_skin_tone_latency, 50),
        ("Face Shape Classification", test_face_shape_latency, 10),
        ("Recommendation Engine", test_recommendation_engine_latency, 100),
        ("Product Discovery", test_product_discovery_latency, 50),
    ]
    
    all_passed = True
    
    for name, func, target_ms in benchmarks:
        try:
            result = func()
            passed = result['mean'] < target_ms
            status = "PASS" if passed else "FAIL"
            if not passed:
                all_passed = False
            
            print(f"\n{name}")
            print(f"  Target: <{target_ms}ms")
            print(f"  Mean:   {result['mean']:.2f}ms")
            print(f"  Median: {result['median']:.2f}ms")
            print(f"  Min:    {result['min']:.2f}ms")
            print(f"  Max:    {result['max']:.2f}ms")
            print(f"  Status: [{status}]")
            
        except Exception as e:
            print(f"\n{name}")
            print(f"  ERROR: {e}")
            all_passed = False
    
    print("\n" + "=" * 70)
    
    # Calculate total pipeline latency
    try:
        skin = test_skin_tone_latency()['mean']
        shape = test_face_shape_latency()['mean']
        rec = test_recommendation_engine_latency()['mean']
        prod = test_product_discovery_latency()['mean']
        
        total = skin + shape + rec + prod
        print(f"TOTAL PIPELINE LATENCY: {total:.2f}ms")
        print(f"Target: <500ms for API, <3000ms for full analysis")
        
        if total < 500:
            print("Status: [EXCELLENT] - Well under target")
        elif total < 3000:
            print("Status: [PASS] - Within acceptable range")
        else:
            print("Status: [FAIL] - Optimization needed")
            all_passed = False
    except:
        pass
    
    print("=" * 70)
    
    return all_passed


if __name__ == "__main__":
    success = run_all_benchmarks()
    sys.exit(0 if success else 1)
