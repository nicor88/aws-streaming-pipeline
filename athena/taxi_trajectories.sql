CREATE DATABASE events;

CREATE EXTERNAL TABLE IF NOT EXISTS events.taxi_trajectories (
  TRIP_ID string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
STORED AS TEXTFILE
LOCATION 's3://streaming-pipeline-dev-output/context=firehose_delivery/';
