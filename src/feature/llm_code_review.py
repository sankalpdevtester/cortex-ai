import { NextApiRequest, NextApiResponse } from 'next';
import { OpenAIAPI } from 'openai';
import { Octokit } from '@octokit/octokit';
import { Cache } from '../utils/cache';
import { CodeReviewInsights } from './code_review_insights';

const openai = new OpenAIAPI({
  apiKey: process.env.OPENAI_API_KEY,
});

const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN,
});

const cache = new Cache();

export const llmCodeReview = async (req: NextApiRequest, res: NextApiResponse) => {
  const { owner, repo, pullRequestNumber } = req.query;

  if (!owner || !repo || !pullRequestNumber) {
    return res.status(400).json({ error: 'Missing required parameters' });
  }

  const pullRequest = await octokit.rest.pulls.get({
    owner: owner as string,
    repo: repo as string,
    pull_number: parseInt(pullRequestNumber as string),
  });

  const code = await getCodeFromPullRequest(pullRequest.data);

  const llmResponse = await openai.createCompletion({
    model: 'code-davinci-002',
    prompt: `Review the following code: ${code}`,
    max_tokens: 2048,
  });

  const reviewInsights = await CodeReviewInsights.generateInsights(llmResponse.data.choices[0].text);

  cache.set(`llm-code-review-${owner}-${repo}-${pullRequestNumber}`, reviewInsights);

  return res.json(reviewInsights);
};

const getCodeFromPullRequest = async (pullRequest: any) => {
  const files = await octokit.rest.pulls.listFiles({
    owner: pullRequest.base.repo.owner.login,
    repo: pullRequest.base.repo.name,
    pull_number: pullRequest.number,
  });

  const code = files.data.map((file: any) => file.contents).join('\n');

  return code;
};

export default llmCodeReview;