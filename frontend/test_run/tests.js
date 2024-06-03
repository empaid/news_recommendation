import { Builder, By } from 'selenium-webdriver';
import { expect } from 'chai';
import { describe, it, before, after } from 'mocha';

const baseUrl = 'http://localhost:3000/React';

describe('React App Test', function() {
  this.timeout(30000);
  let driver;

  before(async function() {
    driver = await new Builder().forBrowser('chrome').build();
  });

  after(async function() {
    await driver.quit();
  });

  it('should reach the homepage', async function() {
    await driver.get(baseUrl);
    const title = await driver.getTitle();
    expect(title).to.include('News');
  });

  it('should reach the business page', async function() {
    await driver.get(`${baseUrl}/business`);
    const bodyText = await driver.findElement(By.tagName('body')).getText();
    expect(bodyText).to.include('Business');
  });

  it('should reach the entertainment page', async function() {
    await driver.get(`${baseUrl}/entertainment`);
    const bodyText = await driver.findElement(By.tagName('body')).getText();
    expect(bodyText).to.include('Entertainment');
  });

  it('should reach the general page', async function() {
    await driver.get(`${baseUrl}/general`);
    const bodyText = await driver.findElement(By.tagName('body')).getText();
    expect(bodyText).to.include('General');
  });

  it('should reach the health page', async function() {
    await driver.get(`${baseUrl}/health`);
    const bodyText = await driver.findElement(By.tagName('body')).getText();
    expect(bodyText).to.include('Health');
  });

  it('should reach the science page', async function() {
    await driver.get(`${baseUrl}/science`);
    const bodyText = await driver.findElement(By.tagName('body')).getText();
    expect(bodyText).to.include('Science');
  });

  it('should reach the sports page', async function() {
    await driver.get(`${baseUrl}/sports`);
    const bodyText = await driver.findElement(By.tagName('body')).getText();
    expect(bodyText).to.include('Sports');
  });

  it('should reach the technology page', async function() {
    await driver.get(`${baseUrl}/technology`);
    const bodyText = await driver.findElement(By.tagName('body')).getText();
    expect(bodyText).to.include('Technology');
  });
});
