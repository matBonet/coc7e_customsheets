# How to use
```python3 src/translator.py {template_path} {parameter_path} {output_path}```

Example:

```python3 src/translator.py templates/coc7eanniversary_firstpage.svg translations/CoC-custom-en.json "CoC 7e Custom Sheet (en)"```

# Deployment
Docker image (based on AWS base image for python) is built and deployed onto AWS Lambda.

## Running local test

Build test image
```docker build -t docker-image:test .```

Start docker image
```docker run -p 9000:8080 docker-image:test```

Call Lambda handler at ```localhost:9000/2015-03-31/functions/function/invocations```