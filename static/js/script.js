document.getElementById('submit').addEventListener('click',processInput)
document.getElementById('clear').addEventListener('click',clear)

//console.log('hlelo is this workign');

async function processInput() {
    equation = document.getElementById('equation').value;
    const container = document.getElementById('image-container');
    const error_msg = document.getElementById('invalid');

    if (equation == '') {
        equation = 'f(x) = sin(x^2) - x/2';
        document.getElementById('equation').value = equation;
    }

    try {
        const response = await fetch('https://graphing-calculator-production.up.railway.app/run_python', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: equation }), 
        });

        const data = await response.json();

        if (response.ok) {
            const img = document.getElementById('image-container');
            img.src = `https://graphing-calculator-production.up.railway.app/static/images/${data.output}`;
            img.loading = 'lazy';

            container.innerHTML = '';

            document.getElementById('result').innerText = ``;
            error_msg.style.visibility = 'hidden';
        } else {
            error_msg.style.visibility = 'visible';
        }
    } catch (error) {
        console.error('Error:', error);
    }
}


function clear() {
    document.getElementById('equation').value = '';
    document.getElementById('image-container').src = 'https://graphing-calculator-production.up.railway.app/static/images/placeholder.png';
    error_msg.style.visibility = 'hidden';
}
