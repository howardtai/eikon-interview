#!/bin/bash
# Execute the queries and print response

echo "Total experiments each user ran:"
curl http://localhost:80/total_experiments
echo ""

echo "Average experiments per user:"
curl http://localhost:80/average_experiments
echo ""

echo "Most commonly experimented compound:"
curl http://localhost:80/most_common_compound
echo ""