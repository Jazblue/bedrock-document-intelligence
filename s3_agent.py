from s3_manager import download_document
from agent import process_document
from database import (
    save_result,
    start_processing,
    mark_failed
)
from logger import logger


def process_s3_document(filename):

    logger.info(
        f"Processing S3 document: {filename}"
    )

    start_processing(filename)

    try:

        local_file = download_document(filename)

        logger.info(
            f"Downloaded document: {filename}"
        )

        result = process_document(local_file)

        logger.info(
            f"Document processing completed: {filename}"
        )

        save_result(
            filename,
            result
        )

        logger.info(
            f"Saved result to DynamoDB: {filename}"
        )

        return result

    except Exception as error:

        logger.error(
            f"Processing failed for {filename}: {error}"
        )

        mark_failed(
            filename,
            error
        )

        return {
            "error": "Document processing failed",
            "details": str(error)
        }