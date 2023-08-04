# Eikon Takehome

### Requirements
This application uses docker-compose to create a dockerized ETL app. Make sure to install docker-compose. 

Use `chmod +x` to set the scripts under `scripts/` :  [ `build_and_run.sh`, `trigger_etl.sh`, `run_queries.sh` ] as executable.

Navigate working directory to this folder to begin.

### Build and Run

Run the following to bring up the application, which will then be served at `http://localhost:80`.
```bash
./scripts/build_and_run.sh
```

### Trigger the ETL Process

After the application is running, run the following to trigger the ETL process. 

```bash
./scripts/trigger_etl.sh
```

This will send a POST request to the `/trigger_etl` api, starting the ETL process. The application will load the CSV files from the `data` directory, process them, and upload the processed data into the PostgreSQL database.

### Execute Database Queries

After the ETL process is completed, run the following to obtain database queries that provides the requested features:

```bash
./scripts/execute_queries.sh
```

This will send GET requests to the `/total_experiments`, `/average_experiments`, and `/most_common_compound` api and print the responses. These responses contain the total number of experiments each user has run, the average number of experiments per user, and the most commonly used compound, respectively.
