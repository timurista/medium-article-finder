#!/usr/bin/env node
import 'source-map-support/register';
import cdk = require('@aws-cdk/core');
import { MediumArticleScraperStack } from '../lib/medium-article-scraper-stack';

const app = new cdk.App();
new MediumArticleScraperStack(app, 'MediumArticleScraperStack');
