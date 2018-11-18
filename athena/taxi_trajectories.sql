CREATE DATABASE events;

DROP TABLE IF EXISTS events.taxi_trajectories;
CREATE EXTERNAL TABLE IF NOT EXISTS events.taxi_trajectories (
  TRIP_ID string,
  CALL_TYPE string,
  ORIGIN_CALL string,
  ORIGIN_STAND string,
  TAXI_ID int,
  TIMESTAMP int,
  DAY_TYPE string,
  MISSING_DATA string,
  POLYLINE string,
  EVENT_ID string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
STORED AS TEXTFILE
LOCATION 's3://streaming-pipeline-dev-output/context=firehose_delivery/';
