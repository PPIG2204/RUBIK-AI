import main
import Astar
import random
import time

def generate_random_scramble(depth):
    """Generate random scramble sequence of given depth"""
    moves = ["R", "R'", "L", "L'", "U", "U'", "D", "D'", "F", "F'", "B", "B'"]
    scramble = []
    
    for _ in range(depth):
        # Avoid consecutive same face rotations for realistic scrambles
        move = random.choice(moves)
        if scramble:
            while Astar.get_face_from_move(move) == Astar.get_face_from_move(scramble[-1]):
                move = random.choice(moves)
        scramble.append(move)
    
    return scramble

def stress_test():
    """Run stress tests with different scramble depths"""
    depths = [5, 6, 7]
    num_tests_per_depth = 3  # Test each depth 3 times
    
    print("=" * 80)
    print("RUBIK'S CUBE A* SOLVER - STRESS TEST")
    print("=" * 80)
    print(f"\nTesting {num_tests_per_depth} cases for each depth\n")
    
    results = {depth: [] for depth in depths}
    
    for depth in depths:
        print(f"\n{'='*80}")
        print(f"Testing depth: {depth}")
        print(f"{'='*80}")
        
        for test_num in range(1, num_tests_per_depth + 1):
            print(f"\nTest {test_num}/{num_tests_per_depth}:", end=" ")
            
            # Generate random cube
            cube = main.RubikCube()
            scramble = generate_random_scramble(depth)
            
            print(f"Scramble: {' '.join(scramble)}")
            
            # Apply scramble
            main.use_scramble(cube, scramble)
            
            # Reset global step counter
            Astar.step = 0
            
            # Run A* solver
            print(f"  Solving...", end=" ", flush=True)
            result = Astar.astar(cube.cube)
            
            if result:
                solution, nodes_expanded, elapsed_time = result
                solution_length = len(solution) if solution else 0
                print(f"✓ Found solution in {solution_length} moves")
                print(f"    Nodes expanded: {nodes_expanded:,}")
                print(f"    Time: {elapsed_time:.4f}s")
                
                results[depth].append({
                    'moves': solution_length,
                    'nodes': nodes_expanded,
                    'time': elapsed_time,
                    'scramble': scramble
                })
            else:
                print(f"✗ No solution found")
                results[depth].append({
                    'moves': -1,
                    'nodes': -1,
                    'time': -1,
                    'scramble': scramble
                })
    
    # Print summary
    print(f"\n\n{'='*80}")
    print("SUMMARY REPORT")
    print(f"{'='*80}\n")
    
    print(f"{'Depth':<8} {'Avg Moves':<12} {'Avg Nodes':<15} {'Avg Time (s)':<15}")
    print("-" * 50)
    
    for depth in depths:
        if results[depth]:
            valid_results = [r for r in results[depth] if r['moves'] >= 0]
            if valid_results:
                avg_moves = sum(r['moves'] for r in valid_results) / len(valid_results)
                avg_nodes = sum(r['nodes'] for r in valid_results) / len(valid_results)
                avg_time = sum(r['time'] for r in valid_results) / len(valid_results)
                
                print(f"{depth:<8} {avg_moves:<12.1f} {avg_nodes:<15,.0f} {avg_time:<15.6f}")
    
    print("\n" + "=" * 80)
    print("Detailed Results:")
    print("=" * 80)
    
    for depth in depths:
        print(f"\nDepth {depth}:")
        print(f"{'Test':<8} {'Solution':<12} {'Nodes':<15} {'Time (s)':<15}")
        print("-" * 50)
        
        for i, result in enumerate(results[depth], 1):
            if result['moves'] >= 0:
                print(f"{i:<8} {result['moves']:<12} {result['nodes']:<15,} {result['time']:<15.6f}")
            else:
                print(f"{i:<8} {'FAILED':<12} {'-':<15} {'-':<15}")

if __name__ == "__main__":
    stress_test()
