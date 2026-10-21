mkdir -p ~/.streamlit/

ech "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" >/.streamlit/config.toml