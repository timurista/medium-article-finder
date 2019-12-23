import { expect as expectCDK, matchTemplate, MatchStyle } from '@aws-cdk/assert';
import cdk = require('@aws-cdk/core');
import MediumArticleScraper = require('../lib/medium-article-scraper-stack');

test('Empty Stack', () => {
    const app = new cdk.App();
    // WHEN
    const stack = new MediumArticleScraper.MediumArticleScraperStack(app, 'MyTestStack');
    // THEN
    expectCDK(stack).to(matchTemplate({
      "Resources": {}
    }, MatchStyle.EXACT))
});