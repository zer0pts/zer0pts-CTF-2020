// (snipped)

const flag = 'zer0pts{<censored>}';

// (snipped)

const crawl = async (url) => {
    console.log(`[+] Query! (${url})`);
    const page = await browser.newPage();
    try {
        await page.setUserAgent(flag);
        await page.goto(url, {
            waitUntil: 'networkidle0',
            timeout: 10 * 1000,
        });
        await page.click('#like');
    } catch (err){
        console.log(err);
    }
    await page.close();
    console.log(`[+] Done! (${url})`)
};

// (snipped)