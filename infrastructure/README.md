# The AWS Bedrock Playground Infrastructure

First you need to ...

- set your AWS_PROFILE with `export AWS_PROFILE=...`
- then you need to login to the right pulumoi account with `pulumi login`
- and then you need to make sure the right stack (`aws-bedrock-playground`) is selected by running `pulumi stack ls` (potentially follow by `pulumi stack select aws-bedrock-playground`)

To make this work you need to run ...

```bash
uv sync
pulumi preview
pulumi up --yes
```

Do not forget to tear down the infrastructure after/when you are done (with `pulumi destroy`).
