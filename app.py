Refactor the current Streamlit codebase into a single, production-ready workspace file named strictly 'app.py'. The entire application must combine advanced image filtering and fully dynamic QR code generation engines into a cohesive web interface. Do not generate multiple files; all frontend states, logic, and rendering pipelines must exist in 'app.py' to run on Streamlit Cloud using only 'streamlit', 'Pillow', and 'segno' inside requirements.txt.

Implement the following architecture inside the app:

1. WORKSPACE NAVIGATION
- Setup a clean sidebar or top navigation system to seamlessly toggle between two functional modes: "🎨 Advanced Image Studio" and "🔮 Universal QR Engine".

2. MODE A: ADVANCED IMAGE STUDIO
- File Uploader: Support standard formats (.png, .jpg, .jpeg).
- Enhanced Filters Panel: Retain "Original", "Black & White", "Sepia Tone", "Gaussian Blur", and "Contour Sketch". Add at least three new high-fidelity filter states: "Vibrant Saturation" (Color Enhance), "Retro Negative" (Invert), and "Emboss Art".
- Direct Manipulation Canvas Tools:
  * Crop: Add numeric slice configurations or pixel boundary selectors to crop top/bottom/left/right boundaries.
  * Resize: Provide interactive inputs/sliders to adjust Width and Height dimensions while maintaining or modifying scale.
  * Image Compression Engine: Add a quality slider (1-100) that modifies the byte weight of the file before saving, outputting the dynamic file size optimization metrics live on screen.
- Export Pipeline: Keep the side-by-side comparison layout and a functional download button for the modified image array.

3. MODE B: UNIVERSAL QR ENGINE
- Split the interface into three explicit structural pipelines:
  * Text to QR: Input raw paragraphs. When scanned, it must directly display the raw literal text safely on the scanner's screen.
  * Link to QR: Input website URLs. When scanned, it must natively redirect the device to the absolute target web page.
  * Image to QR Pipeline (Convert Image to QR): Allow users to upload an image file. The engine must immediately convert the binary image into a Base64-encoded URI string data block and write it directly into a high-capacity QR code matrix. When scanned, the device should render the encoded payload text string or attempt to resolve the asset.
- Styling Overrides: Maintain the sidebar color picker mechanics for line color (dark) and background canvas color (light).
- Download Engine: Keep the functional download action block for the compiled output file.

Enforce strict 'try-except' containment shielding blocks around all heavy processing logic (Base64 encoding, matrix generation, image convolution steps) to intercept and print descriptive warning flags directly onto the web UI canvas rather than allowing the application shell to crash. Use clean markdown formatting elements throughout to organize the screen grid layout beautifully.
