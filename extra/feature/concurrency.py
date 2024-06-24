'''
  - Parallel Programming  : running multiple tasks at the same time, where share of processing units (2 lines of customers in 2 cashiers)
  - Conccurency           : switching for makes progress of more tasks at the same time (2 lines of customers in a cashier)
  
  Parallelism in Python -> Global Interpreter Lock (GIL), but Python are single threaded
  Python are good in Conccurency
  
'''


from __future__ import annotations
import sys, functools, asyncio
from pathlib import Path

# Development
sys.path.append(Path.cwd().as_posix())
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def main():
  return {"message":"Hello World"}