from BiocLoader import BiocLoader
from Pipeline import Pipeline


def run(training_data_file, output_dir):
    # Parse data
    loader = BiocLoader()
    data = loader.parse(training_data_file)

    # Run Train
    pipeline = Pipeline()
    pipeline.run_model(data_rows=data, output_dir=output_dir)
