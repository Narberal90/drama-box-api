FROM python:3.12

LABEL authors="mordegear90@gmail.com"

WORKDIR /app

ENV PYTHONBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt




RUN mkdir -p /vol/web/media

RUN adduser --disabled-password --no-create-home user_unit
RUN chown -R user_unit:user_unit /vol/
RUN chmod -R 755 /vol/web

USER user_unit

COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "drama_box_api.wsgi:application"]
