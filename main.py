const runkitExpress = require("@runkit/runkit/express-endpoint/1.0.0");
const bodyParser = require('body-parser');
const app = runkitExpress(exports);

app.set('json spaces', 2);
app.use(require('compression')())
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));
const { M1Z_URL, API_M1Z_KEY, MY_APP_KEY, RUNKIT_ENDPOINT_URL } = process.env;

// add CORS headers, so the API is available anywhere
app.use(function(req, res, next)
{
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Expose-Headers", "runkit-rate-limit-remaining");
    res.header("Access-Control-Expose-Headers", "tonic-rate-limit-remaining");

    var reqHeaders = req.get("Access-Control-Request-Headers");
    if (reqHeaders) res.header("Access-Control-Allow-Headers", reqHeaders);

    var reqMethods = req.get("Access-Control-Request-Methods");
    if (reqMethods) res.header("Access-Control-Allow-Methods", reqMethods);

    next();
})

function emoji(texto){
    linhas = texto.split('\n')
    t = linhas.map((l) => Array.from(l.matchAll(/(.*?)(&#x)([0-9,A,B,C,D,E,F]*);/gi)))
    rlinha = '';
    for (l in t){
        for (x in t[l]){
            rlinha += t[l][x][1]+String.fromCodePoint('0x'+t[l][x][3])
        }
        ac = '';
        ini = t[l].reduce(
            (accumulator, currentValue) => accumulator + currentValue[0],
            ac
        )
        rlinha += linhas[l].substring(ini.length)+'\n'
    }    
    return rlinha.substring(0,rlinha.length-1)
}

async function messages(req, res) {
    let token = req.query.token;
    if (token != MY_APP_KEY) {
        res.send(403,"You do not have rights to visit this page");
        return
    }
    let options = {
        'method' : 'POST',
        'headers': {
            'content-type': 'application/json',
            'accept': 'application/json',
            'Authorization': 'Bearer '+API_M1Z_KEY
        },
        'body': JSON.stringify({
            'text' : emoji(req.body.text),
            'dontOpenTicket' : 'true',
            'origin':'bot',
            'contactId' : req.body.contactId})
    }
    //let tokenSAC = await (await fetch()).text();
    let enviou = await (await fetch(M1Z_URL +'/messages',options)).json();
    res.send(JSON.stringify(enviou));
}
app.post("/messages", messages);
