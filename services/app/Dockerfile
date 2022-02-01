# ----------------BUILDER------------------------------
# pull official base image
FROM python:3.9.5-slim-buster AS builder

# Work directory
WORKDIR /usr/src/app

# Environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Install system depencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc 

# lint 
RUN pip install --upgrade pip 
RUN pip install flake8===3.9.1
COPY . /usr/src/app/

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


# -----------------------------------------------
FROM python:3.9.5-slim-buster AS final
# create directory for the app user
# RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/

WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
# First run login as we are using app as user not root
RUN chmod +x /home/app/entrypoint.sh
ENTRYPOINT ["sh","/home/app/entrypoint.sh"]
