#!/bin/bash

METRICS_DIR="../metrics"

read -p "Are you sure you want to delete all files in the metrics directory? Type 'YES' to confirm: " confirm

if [[ $confirm == "YES" ]]; then
  if [ -d "$METRICS_DIR" ]; then
    rm -rf "$METRICS_DIR"/*
    echo "All files have been deleted from the metrics directory."
  else
    echo "The metrics directory does not exist."
  fi
else
  echo "Deletion cancelled by user."
fi
