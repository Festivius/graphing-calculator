
document.getElementById('submit').addEventListener('click',processInput)
document.getElementById('clear').addEventListener('click',clear)

console.log('hlelo is this workign');

async function processInput() {
    equation = document.getElementById('equation').value;
    const container = document.getElementById('image-container');
    const error_msg = document.getElementById('invalid');

    console.log(equation);
    console.log(JSON.stringify({ input: equation }))

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
            console.log(img);
            img.src = `http://127.0.0.1:5000/${data.output}`;
            img.loading = 'lazy';

            console.log(img);

            container.innerHTML = '';

            document.getElementById('result').innerText = ``;
            error_msg.style.visibility = 'hidden';
        } else {
            //document.getElementById('result').innerText = `Error: ${data.error}`;
            error_msg.style.visibility = 'visible';
        }
    } catch (error) {
        console.error('Error:', error);
        //document.getElementById('result').innerText = 'An error occurred.';
    }
}


function clear() {
    document.getElementById('equation').value = '';
    document.getElementById('image-container').src = 'placeholder.png';
}
