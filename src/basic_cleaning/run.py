#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    logger.info("Data cleaning is started: ")
    df = pd.read_csv(artifact_local_path)
    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    df.to_csv("clean_sample.csv", index=False)
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")
    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="input artifact to the pipeline",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="output artifact of this pipeline",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="clean_data",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="clean_data",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="minimum value for price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="maximum value for price",
        required=True
    )

    args = parser.parse_args()
    go(args)
