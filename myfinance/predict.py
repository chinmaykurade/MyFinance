import logging

from myfinance import pipeline

_logger = logging.getLogger(__name__)


# %%
def make_prediction(*, input_data, type):
    pipeline.stocks_pipe.fit(X=input_data, y=type)

    results = pipeline.stocks_pipe.predict(X=input_data)

    return results


# %%
if __name__ == '__main__':
    my_results = make_prediction(input_data=None, type='greenblatt')
