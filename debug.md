
INFO:unified_api:Model loading completed!
INFO:     Application startup complete.
INFO:     127.0.0.1:50406 - "GET /health HTTP/1.1" 200 OK
✅ API is ready!
🎨 Starting Streamlit frontend...

============================================================
✅ System started successfully!
============================================================
🔗 Access URLs:
   📊 API Documentation: http://localhost:8000/docs
   🎨 Frontend Application: http://localhost:8501
   ❤️ API Health Check: http://localhost:8000/health
   📋 Model Information: http://localhost:8000/models/info
============================================================
📝 Available API Endpoints:
   🌿 Plant Disease: POST /predict/plant-disease
   🌾 Paddy Disease: POST /predict/paddy-disease
   🐛 Pest Classification: POST /predict/pest
   🔀 Unified (Placeholder): POST /predict/unified
============================================================
⚠️  Press Ctrl+C to stop all services
============================================================

  You can now view your Streamlit app in your browser.

  URL: http://0.0.0.0:8501

🌐 Opening browser...
INFO:     127.0.0.1:50421 - "GET /docs HTTP/1.1" 200 OK
INFO:     127.0.0.1:50454 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:50422 - "GET /openapi.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:50501 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:50503 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:50505 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:50540 - "GET /health HTTP/1.1" 200 OK
INFO:     127.0.0.1:50547 - "GET /health HTTP/1.1" 200 OK
2025-06-27 00:42:31.414 Uncaught app exception
Traceback (most recent call last):
  File "C:\Users\premo\AppData\Local\Programs\Python\Python311\Lib\site-packages\streamlit\runtime\scriptrunner\script_runner.py", line 534, in _run_script
    exec(code, module.__dict__)
  File "D:\Projects\Portfolio projects\Agri-tech Hackathon\Backend\unified_frontend.py", line 335, in <module>
    main()
  File "D:\Projects\Portfolio projects\Agri-tech Hackathon\Backend\unified_frontend.py", line 254, in main
    st.image(image, caption="Uploaded Plant Image", use_container_width=True)
  File "C:\Users\premo\AppData\Local\Programs\Python\Python311\Lib\site-packages\streamlit\runtime\metrics_util.py", line 396, in wrapped_func 
    result = non_optional_func(*args, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: ImageMixin.image() got an unexpected keyword argument 'use_container_width'
