{{ config(materialized='view') }}

select *
from {{ source {stagging},{passenger-records} }}