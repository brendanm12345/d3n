# d3n
D3N is the first-ever orchestration framework for managing a fleet of parallel devin workers. We break a github repository down into a set of isolated github issues that can be solved concurrently and then optimally assign issues to each worker to minimize the mean completion time and maximize bandwidth. This is achieved through a sophisticated server mechanism that dynamically routes tasks to worker Devin nodes, ensuring optimal utilization of resources and faster delivery of results.

- We tried to solve some of the biggest pain points that people experience using devin:
    - It can be slow - our system can 10x speed through parallelization
    - It can fail - our system support automatic retries for failed jobs (+ ReAct reflection to improve reasoning)
    


![ScreenRecording2024-05-05at2 33 05PM-ezgif com-video-to-gif-converter (1)](https://github.com/brendanm12345/d3n/assets/72267866/69ac2384-4b92-477c-9b58-93d81273ba8e)

## Demo
Watch a live demo of the project: https://twitter.com/SohamGovande/status/1787213625880609112

## Architecture
Worker task success and failure behavior
![image](https://github.com/brendanm12345/d3n/assets/72267866/42112a61-9142-477e-b52e-e865d6523c30)

Orchestrator Devin micromanaging worker Devin after failure
![image](https://github.com/brendanm12345/d3n/assets/72267866/4bb7a083-b41a-40d5-9910-d33d34182f0d)
