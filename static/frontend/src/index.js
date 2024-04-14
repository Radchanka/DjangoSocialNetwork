import 'bootstrap/dist/css/bootstrap.css';

document.addEventListener('DOMContentLoaded', async () => {
  console.log('Hello');


  const currentPage = window.location.pathname.split('/').pop();

  try {
    const { default: pageScript } = await import(`./pages/${currentPage}.js`);
    if (typeof pageScript === 'function') {
      pageScript();
    }
  } catch (error) {
    console.error('Error loading page script:', error);
  }
});