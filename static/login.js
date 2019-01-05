const url = new URL(window.location.href);
const c = url.searchParams.get('login');
if (c === 'failed') {
    const ele = document.createElement('h2');
    ele.style = 'color: #fc6c6c; font-family: sans-serif';
    ele.textContent = 'Incorrect Username or Password!';
    document.body.insertBefore(ele, document.getElementsByTagName('form')[0])
}