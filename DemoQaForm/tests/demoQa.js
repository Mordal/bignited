const { WebElement } = require("selenium-webdriver");
const {By,Key,Builder} = require("selenium-webdriver");
require("chromedriver");

// Require chai.js expect module for assertions
const chai = require('chai');
const expect = require('chai').expect;
const assert = require('chai').assert;


async function Form(){

    //To wait for browser to build and launch properly
    let driver = await new Builder().forBrowser("chrome").build();
    
    //Fetching demoqa.com practice form
    await driver.get("https://demoqa.com/automation-practice-form");

    //fill in form
    await driver.findElement(By.id("firstName")).sendKeys("Pieter");
    await driver.findElement(By.id("lastName")).sendKeys("De Bie");
    //Label to be used because it overlaps the radio-button and the button itself can't be clicked
    driver.findElement(By.className("custom-control-label")).click();
    //use Enter key to submit
    await driver.findElement(By.id("userNumber")).sendKeys("0496392399",Key.ENTER);

    //check if popup is present
    driver.findElements(By.className("modal-content")).then(function(webElement){
        assert.isNotEmpty(webElement,"Web element is not present")
    });

}

Form();
