// Parses the game script so a syntax error is caught before it ships.  Usage: node tools/syntax_check.js
const fs = require('fs'), vm = require('vm'), path = require('path');
const s = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const i = s.lastIndexOf('<script>'), j = s.lastIndexOf('</script>');
try { new vm.Script(s.slice(i + 8, j), { filename: 'game.js' }); console.log('syntax ok'); }
catch (e) { console.log(e.stack.split('\n').slice(0, 5).join('\n')); process.exit(1); }
