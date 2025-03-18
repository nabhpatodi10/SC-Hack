from langchain.schema.runnable import RunnableParallel, RunnableLambda

from face_identification import FaceIdentification
from attachment_preprocessing import AttachmentPreprocessing
from tools import Tools
from agent import Agent