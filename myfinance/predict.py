import logging

from myfinance import pipeline

_logger = logging.getLogger(__name__)


# %%
def make_prediction(*, input_data):
    pipeline.stocks_pipe.fit(input_data, None)

    results = pipeline.stocks_pipe.predict(input_data)

    return results


# %%
if __name__ == '__main__':
    my_results = make_prediction(input_data=None)
