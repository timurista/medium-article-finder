import cdk = require('@aws-cdk/core');
import events = require("@aws-cdk/aws-events");
import targets = require("@aws-cdk/aws-events-targets");
import lambda = require("@aws-cdk/aws-lambda");
import path = require("path");
import iam = require("@aws-cdk/aws-iam");

export class MediumArticleScraperStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const s3ReadWritePolicy = new iam.PolicyStatement({
      effect: iam.Effect.ALLOW,
      actions: ["s3:*"],
      resources: ["*"]
    });

    const lambdaFn = new lambda.Function(this, "blogPostAggregator", {
      runtime: lambda.Runtime.PYTHON_3_7,
      handler: "lambda_handler.main",
      code: new lambda.AssetCode(path.join(__dirname, "build-src")),
      timeout: cdk.Duration.seconds(50),
      environment: {
        BUCKET: "www.thetimurista.com",
        CACHE_BUCKET: 'tim-urista-web-blog-articles-distribution-v1'
      }
    });

    lambdaFn.addToRolePolicy(s3ReadWritePolicy);

      // Run every 3 hours a day
      // See https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html
      new events.Rule(this, "Rule", {
        schedule: events.Schedule.expression("cron(12 3 ? * * *)"),
        targets: [new targets.LambdaFunction(lambdaFn)]
      });
    // The code that defines your stack goes here
  }
}
