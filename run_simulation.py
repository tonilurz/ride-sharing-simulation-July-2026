import argparse
import random

from simulation import Simulation


def main():
    """
    Runs the final ride-sharing simulation
    using command-line configuration options.
    """

    # -------------------------------------------------
    # CREATE COMMAND-LINE ARGUMENT PARSER
    # -------------------------------------------------

    parser = argparse.ArgumentParser(
        description="Final Ride-Sharing Simulator"
    )

    # Maximum simulation time for generating riders
    parser.add_argument(
        "--max-time",
        type=float,
        default=500,
        help="Maximum time for generating new rider requests."
    )

    # Maximum number of riders to generate
    parser.add_argument(
        "--num-riders",
        type=int,
        default=50,
        help="Maximum number of riders to generate."
    )

    # Number of cars in the fleet
    parser.add_argument(
        "--num-cars",
        type=int,
        default=5,
        help="Number of cars to create."
    )

    # Number of nearby Quadtree candidates
    parser.add_argument(
        "--candidate-count",
        type=int,
        default=5,
        help="Number of nearby cars evaluated with Dijkstra."
    )

    # Random seed for repeatable results
    parser.add_argument(
        "--random-seed",
        type=int,
        default=42,
        help="Random seed used for repeatable simulation results."
    )

    # City map file
    parser.add_argument(
        "--map-file",
        type=str,
        default="city_map.csv",
        help="Path to the unified city map CSV file."
    )

    # Read command-line arguments
    args = parser.parse_args()

    # -------------------------------------------------
    # SET RANDOM SEED
    # -------------------------------------------------

    random.seed(
        args.random_seed
    )

    # -------------------------------------------------
    # CREATE SIMULATION
    # -------------------------------------------------

    simulation = Simulation(
        map_filename=args.map_file,
        max_time=args.max_time,
        num_riders=args.num_riders,
        candidate_count=args.candidate_count
    )

    # -------------------------------------------------
    # CREATE INITIAL CARS
    # -------------------------------------------------

    simulation.initialize_cars(
        args.num_cars
    )

    # -------------------------------------------------
    # OPTIONAL INITIALIZATION CHECK
    # Remove later if you do not want this printed
    # -------------------------------------------------

    print(
        f"Cars created: {len(simulation.cars)}"
    )

    print(
        f"Available cars: "
        f"{len(simulation.available_cars)}"
    )

    print(
        f"Available car points: "
        f"{len(simulation.available_car_points)}"
    )

    # -------------------------------------------------
    # RUN SIMULATION
    # -------------------------------------------------

    simulation.run()

    # -------------------------------------------------
    # PRINT FINAL METRICS
    # -------------------------------------------------

    simulation.print_metrics()

    # -------------------------------------------------
    # CREATE REQUIRED PNG
    # -------------------------------------------------

    simulation.create_summary_visualization()


if __name__ == "__main__":
    main()