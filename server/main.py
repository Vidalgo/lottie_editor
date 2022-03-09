from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.server import RequestParameters, Response
from engine.lottie_animation_manipulator import Lottie_animation_manipulator, Lottie_animation

import logging
logger = logging.getLogger(__name__)


app = FastAPI(description="Lottie Engine", version="1.0.0", title="Lottie Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/process')
def post_calculate(params: RequestParameters) -> Response:
    logger.info('processing request')
    animation = Lottie_animation()
    animation.load(params.animation)
    engine = Lottie_animation_manipulator(lottie_animation=animation, all_lottie_operations=params.operations)
    engine.apply_operations_on_elements()
    return Response(animation=engine.lottie.lottie_base)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5555, access_log=False)
