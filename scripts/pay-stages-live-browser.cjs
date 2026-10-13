const {chromium}=require('../app/node_modules/playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
(async()=>{
if (!process.env.OFFICE_TEST_PASSWORD) throw new Error('Set OFFICE_TEST_PASSWORD for the disposable test account');
 const login=await fetch('http://127.0.0.1:8099/api/v1/authentication/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({NationalId:'000000000000',Password:process.env.OFFICE_TEST_PASSWORD})});assert.equal(login.status,200);
 const auth=await login.json(),token=auth.token??auth.accessToken;
 const evidence=JSON.parse(fs.readFileSync('evidence/phase4-roundtrip.json'));
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium-browser',headless:true});
 try{
 const context=await browser.newContext({viewport:{width:1440,height:1000}});
 await context.addCookies([{name:'kt-xnk-access-token',value:token,url:'http://localhost:3002'},{name:'kt-xnk-session-permissions',value:'["logistics:contracts:view","logistics:contracts:manage","logistics:view"]',url:'http://localhost:3002'}]);
 const page=await context.newPage();page.setDefaultTimeout(15000);page.on('console',m=>{if(m.type()==='error')console.log('BROWSER_ERROR',m.text().slice(0,200));});
 await page.goto(`http://localhost:3002/logistics/contract/${evidence.contractId}`);
 await page.getByText('Second part edited',{exact:true}).waitFor();
 await page.getByRole('button',{name:'Chỉnh sửa',exact:true}).click();
 console.log('TEXTAREAS',JSON.stringify(await page.locator('textarea').evaluateAll(nodes=>nodes.map(e=>({id:e.id,value:e.value,labels:[...e.labels].map(l=>l.textContent)})))));
 const field=page.getByLabel(/Điều kiện lần 1\.1/);await field.waitFor();
 await field.fill('UI saved occurrence');
 const saved=page.waitForResponse(r=>r.url().includes(`/contracts/${evidence.contractId}`)&&r.request().method()==='PUT');
 await page.getByRole('button',{name:'Lưu thay đổi',exact:true}).click();
 let res;try{res=await saved;}catch(e){await page.screenshot({path:'evidence/phase4-live-debug.png'});console.log('FORM_TEXT',(await page.locator('body').innerText()).slice(-2600));throw e;}assert.equal(res.status(),200,await res.text());
 await page.reload();await page.getByText('UI saved occurrence',{exact:true}).waitFor();
 const verified=await fetch(`http://127.0.0.1:8099/api/v1/contracts/${evidence.contractId}`,{headers:{Authorization:`Bearer ${token}`}});assert.equal(verified.status,200);
 const contract=await verified.json();assert.equal(contract.paymentTerms[0].paymentOccurrences[0].paymentCondition,'UI saved occurrence');assert.equal(contract.paymentTerms[0].paymentOccurrences.length,2);
 for(const width of [1440,390]){await page.setViewportSize({width,height:1000});await page.getByText('UI saved occurrence',{exact:true}).scrollIntoViewIfNeeded();assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true);await page.screenshot({path:`evidence/phase4-live-${width}.png`});}
 fs.writeFileSync('evidence/phase4-live-browser.json',JSON.stringify({FE:evidence.FE,BE:evidence.BE,contractId:evidence.contractId,status:200,condition:'UI saved occurrence',children:contract.paymentTerms[0].paymentOccurrences},null,2)+'\n');
 console.log('PASS real UI edit/save/reload against paired BE; desktop/mobile screenshots and persisted ordered child conditions.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
