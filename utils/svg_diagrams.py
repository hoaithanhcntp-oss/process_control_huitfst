import xml.etree.ElementTree as ET

def get_fopdt_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 180" width="100%" height="180">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#1f77b4" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#fcfcfc" rx="8" stroke="#e0e0e0" stroke-width="1.5"/>
  <text x="375" y="24" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#333" text-anchor="middle">SƠ ĐỒ KHỐI KHÂU QUÁN TÍNH BẬC 1 CÓ TRỄ (FOPDT)</text>
  
  <line x1="50" y1="90" x2="160" y2="90" stroke="#1f77b4" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="105" y="75" font-family="system-ui, sans-serif" font-size="13" font-weight="600" fill="#1f77b4" text-anchor="middle">u(t) / MV</text>
  
  <rect x="170" y="50" width="220" height="80" rx="8" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="280" y="86" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#0d47a1" text-anchor="middle">G(s) = K / (τs + 1)</text>
  <text x="280" y="112" font-family="system-ui, sans-serif" font-size="11" fill="#555" text-anchor="middle">(Khâu quán tính bậc 1)</text>
  
  <line x1="390" y1="90" x2="470" y2="90" stroke="#1f77b4" stroke-width="2.5" marker-end="url(#arrow)"/>
  
  <rect x="480" y="50" width="140" height="80" rx="8" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="550" y="86" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#e65100" text-anchor="middle">e^(-θs)</text>
  <text x="550" y="112" font-family="system-ui, sans-serif" font-size="11" fill="#555" text-anchor="middle">(Khâu trễ thuần θ)</text>
  
  <line x1="620" y1="90" x2="710" y2="90" stroke="#1f77b4" stroke-width="2.5" marker-end="url(#arrow)"/>
  <text x="665" y="75" font-family="system-ui, sans-serif" font-size="13" font-weight="600" fill="#1f77b4" text-anchor="middle">y(t) / PV</text>
  
  <text x="375" y="158" font-family="system-ui, sans-serif" font-size="11" fill="#666" text-anchor="middle">💡 Tại thời điểm t = θ + τ, đáp ứng đạt 63.2% giá trị xác lập K</text>
</svg>"""

def get_second_order_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 180" width="100%" height="180">
  <defs>
    <marker id="arrow_so" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#6a1b9a" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#fcfcfc" rx="8" stroke="#e0e0e0" stroke-width="1.5"/>
  <text x="375" y="24" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#333" text-anchor="middle">SƠ ĐỒ KHỐI HỆ DAO ĐỘNG BẬC 2 CHUẨN</text>
  
  <line x1="60" y1="90" x2="200" y2="90" stroke="#6a1b9a" stroke-width="2.5" marker-end="url(#arrow_so)"/>
  <text x="130" y="75" font-family="system-ui, sans-serif" font-size="13" font-weight="600" fill="#6a1b9a" text-anchor="middle">r(t) / Tín hiệu vào</text>
  
  <rect x="210" y="45" width="340" height="90" rx="8" fill="#f3e5f5" stroke="#8e24aa" stroke-width="2"/>
  <text x="380" y="83" font-family="system-ui, sans-serif" font-size="15" font-weight="bold" fill="#4a148c" text-anchor="middle">G(s) = ωn² / (s² + 2ζωn·s + ωn²)</text>
  <text x="380" y="112" font-family="system-ui, sans-serif" font-size="11" fill="#555" text-anchor="middle">ωn: Tần số dao động tự nhiên | ζ: Hệ số tắt dần (Damping Ratio)</text>
  
  <line x1="550" y1="90" x2="690" y2="90" stroke="#6a1b9a" stroke-width="2.5" marker-end="url(#arrow_so)"/>
  <text x="620" y="75" font-family="system-ui, sans-serif" font-size="13" font-weight="600" fill="#6a1b9a" text-anchor="middle">y(t) / Đáp ứng</text>
  
  <text x="375" y="158" font-family="system-ui, sans-serif" font-size="11" fill="#666" text-anchor="middle">Phân loại: ζ = 0 (Không tắt) | 0 &lt; ζ &lt; 1 (Thiếu suy giảm) | ζ = 1 (Tới hạn) | ζ &gt; 1 (Quá suy giảm)</text>
</svg>"""

def get_step_metrics_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 240" width="100%" height="240">
  <defs>
    <marker id="arrow_m" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#333" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#fafafa" rx="8" stroke="#e0e0e0" stroke-width="1.5"/>
  <text x="375" y="24" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#333" text-anchor="middle">ĐỊNH NGHĨA CÁC CHỈ TIÊU CHẤT LƯỢNG QUÁ ĐỘ TRÊN ĐÁP ỨNG BƯỚC NHẢY</text>
  
  <!-- Axes -->
  <line x1="80" y1="200" x2="700" y2="200" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_m)"/>
  <line x1="80" y1="200" x2="80" y2="40" stroke="#333" stroke-width="1.5" marker-end="url(#arrow_m)"/>
  <text x="690" y="220" font-family="sans-serif" font-size="11" fill="#333">Thời gian t</text>
  <text x="60" y="45" font-family="sans-serif" font-size="11" fill="#333">y(t)</text>
  
  <!-- Steady state line y_ss = 1 -->
  <line x1="80" y1="120" x2="680" y2="120" stroke="red" stroke-width="1.5" stroke-dasharray="4,4"/>
  <text x="640" y="112" font-family="sans-serif" font-size="10" font-weight="bold" fill="red">r(t) = 1.0 (SP)</text>
  
  <!-- Tolerance Band ±2% -->
  <line x1="80" y1="115" x2="680" y2="115" stroke="gray" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="80" y1="125" x2="680" y2="125" stroke="gray" stroke-width="1" stroke-dasharray="2,2"/>
  <text x="635" y="137" font-family="sans-serif" font-size="9" fill="gray">Dải ±2%</text>
  
  <!-- Step response curve -->
  <path d="M 80 200 C 130 190, 160 140, 220 70 C 260 20, 290 140, 360 110 C 420 85, 470 123, 540 120 L 680 120" fill="none" stroke="#1f77b4" stroke-width="2.5"/>
  
  <!-- Peak Overshoot -->
  <line x1="220" y1="70" x2="220" y2="200" stroke="#d32f2f" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="80" y1="70" x2="220" y2="70" stroke="#d32f2f" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="220" y="60" font-family="sans-serif" font-size="11" font-weight="bold" fill="#d32f2f" text-anchor="middle">y_max (Độ vọt lố %OS)</text>
  <text x="220" y="215" font-family="sans-serif" font-size="10" font-weight="bold" fill="#d32f2f" text-anchor="middle">Tp (Peak)</text>
  
  <!-- Rise time Tr (10% to 90%) -->
  <line x1="140" y1="192" x2="140" y2="200" stroke="#388e3c" stroke-width="1.5"/>
  <line x1="195" y1="128" x2="195" y2="200" stroke="#388e3c" stroke-width="1.5"/>
  <line x1="140" y1="180" x2="195" y2="180" stroke="#388e3c" stroke-width="1.5"/>
  <text x="167" y="175" font-family="sans-serif" font-size="10" font-weight="bold" fill="#388e3c" text-anchor="middle">Tr</text>
  
  <!-- Settling Time Ts -->
  <line x1="520" y1="115" x2="520" y2="200" stroke="#7b1fa2" stroke-width="1.5" stroke-dasharray="3,3"/>
  <text x="520" y="215" font-family="sans-serif" font-size="10" font-weight="bold" fill="#7b1fa2" text-anchor="middle">Ts (2%)</text>
</svg>"""

def get_s_plane_bode_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 200" width="100%" height="200">
  <rect width="100%" height="100%" fill="#fafafa" rx="8" stroke="#e0e0e0" stroke-width="1.5"/>
  <text x="375" y="22" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#333" text-anchor="middle">MẶT PHẲNG PHỨC S (CỰC - ZERO) &amp; ĐỘ DỰ TRỮ ỔN ĐỊNH BODE</text>
  
  <!-- S-plane box -->
  <g transform="translate(40, 40)">
    <!-- Stable region (Left) -->
    <rect x="0" y="0" width="140" height="130" fill="#e8f5e9" opacity="0.8"/>
    <!-- Unstable region (Right) -->
    <rect x="140" y="0" width="140" height="130" fill="#ffebee" opacity="0.8"/>
    
    <!-- Axes -->
    <line x1="140" y1="0" x2="140" y2="130" stroke="#333" stroke-width="2"/>
    <line x1="0" y1="65" x2="280" y2="65" stroke="#333" stroke-width="1.5"/>
    
    <text x="70" y="25" font-family="sans-serif" font-size="10" font-weight="bold" fill="#2e7d32" text-anchor="middle">ỔN ĐỊNH (Re &lt; 0)</text>
    <text x="210" y="25" font-family="sans-serif" font-size="10" font-weight="bold" fill="#c62828" text-anchor="middle">MẤT ỔN ĐỊNH (Re &gt; 0)</text>
    <text x="145" y="12" font-family="sans-serif" font-size="9" fill="#333">jω</text>
    <text x="270" y="60" font-family="sans-serif" font-size="9" fill="#333">σ (Re)</text>
    
    <!-- Sample Poles X -->
    <text x="90" y="45" font-family="sans-serif" font-size="14" font-weight="bold" fill="#d32f2f">×</text>
    <text x="90" y="95" font-family="sans-serif" font-size="14" font-weight="bold" fill="#d32f2f">×</text>
  </g>
  
  <!-- Bode margin summary -->
  <g transform="translate(370, 40)">
    <rect x="0" y="0" width="340" height="130" rx="6" fill="#fff" stroke="#90caf9" stroke-width="1.5"/>
    <text x="170" y="25" font-family="sans-serif" font-size="12" font-weight="bold" fill="#1565c0" text-anchor="middle">CHỈ TIÊU ĐỘ DỰ TRỮ ỔN ĐỊNH BODE</text>
    <text x="20" y="55" font-family="sans-serif" font-size="11" fill="#333">• <b>Độ dự trữ biên độ (Gain Margin - GM):</b></text>
    <text x="35" y="73" font-family="sans-serif" font-size="10" fill="#555">Đo tại tần số cắt pha ω_pc (nơi pha = -180°). GM &gt; 6 dB là tốt.</text>
    
    <text x="20" y="98" font-family="sans-serif" font-size="11" fill="#333">• <b>Độ dự trữ pha (Phase Margin - PM):</b></text>
    <text x="35" y="116" font-family="sans-serif" font-size="10" fill="#555">Đo tại tần số cắt biên ω_gc (nơi biên độ = 0 dB). PM: 30° - 60°.</text>
  </g>
</svg>"""

def get_pid_loop_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 210" width="100%" height="210">
  <defs>
    <marker id="arrow_pid" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#2e7d32" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#fafafa" rx="8" stroke="#e0e0e0" stroke-width="1.5"/>
  <text x="400" y="24" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#333" text-anchor="middle">SƠ ĐỒ KHỐI VÒNG ĐIỀU KHIỂN KÍN PHẢN HỒI ÂM (FEEDBACK PID)</text>
  
  <line x1="40" y1="80" x2="130" y2="80" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#arrow_pid)"/>
  <text x="80" y="65" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#2e7d32" text-anchor="middle">r(t) / SP (+)</text>
  
  <circle cx="150" cy="80" r="16" fill="#fff" stroke="#333" stroke-width="2"/>
  <line x1="150" y1="69" x2="150" y2="91" stroke="#333" stroke-width="1.5"/>
  <line x1="139" y1="80" x2="161" y2="80" stroke="#333" stroke-width="1.5"/>
  <text x="136" y="74" font-family="sans-serif" font-size="11" font-weight="bold" fill="#2e7d32">+</text>
  <text x="156" y="104" font-family="sans-serif" font-size="13" font-weight="bold" fill="#c62828">-</text>
  
  <line x1="166" y1="80" x2="230" y2="80" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#arrow_pid)"/>
  <text x="198" y="65" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#d32f2f" text-anchor="middle">e(t)</text>
  
  <rect x="240" y="45" width="220" height="70" rx="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="350" y="78" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#1b5e20" text-anchor="middle">C(s) = Kp + Ki/s + Kd·s</text>
  <text x="350" y="100" font-family="system-ui, sans-serif" font-size="10" fill="#444" text-anchor="middle">(Bộ điều khiển PID song song)</text>
  
  <line x1="460" y1="80" x2="530" y2="80" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#arrow_pid)"/>
  <text x="495" y="65" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#2e7d32" text-anchor="middle">u(t) / MV</text>
  
  <rect x="540" y="45" width="150" height="70" rx="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="615" y="78" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#0d47a1" text-anchor="middle">G_plant(s)</text>
  <text x="615" y="100" font-family="system-ui, sans-serif" font-size="10" fill="#444" text-anchor="middle">(Đối tượng điều khiển)</text>
  
  <line x1="690" y1="80" x2="760" y2="80" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#arrow_pid)"/>
  <text x="730" y="65" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#2e7d32" text-anchor="middle">y(t) / PV</text>
  
  <!-- Feedback branch -->
  <circle cx="720" cy="80" r="4" fill="#2e7d32"/>
  <line x1="720" y1="80" x2="720" y2="160" stroke="#2e7d32" stroke-width="2"/>
  <line x1="720" y1="160" x2="150" y2="160" stroke="#2e7d32" stroke-width="2"/>
  <line x1="150" y1="160" x2="150" y2="102" stroke="#2e7d32" stroke-width="2" marker-end="url(#arrow_pid)"/>
  <text x="430" y="180" font-family="system-ui, sans-serif" font-size="11" fill="#555" text-anchor="middle">Phản hồi âm cảm biến đo lường: H(s) = 1</text>
</svg>"""

def get_feedforward_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 240" width="100%" height="240">
  <defs>
    <marker id="arrow_ff" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#d84315" />
    </marker>
    <marker id="arrow_fb" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#1565c0" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#fafafa" rx="8" stroke="#e0e0e0" stroke-width="1.5"/>
  <text x="400" y="24" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#333" text-anchor="middle">SƠ ĐỒ ĐIỀU KHIỂN PHẢN HỒI KẾT HỢP TRUYỀN THẲNG (FEEDBACK + FEEDFORWARD)</text>
  
  <line x1="50" y1="60" x2="180" y2="60" stroke="#d84315" stroke-width="2.5" marker-end="url(#arrow_ff)"/>
  <text x="115" y="48" font-family="system-ui, sans-serif" font-size="11" font-weight="bold" fill="#d84315" text-anchor="middle">Nhiễu tải d(t) / DV</text>
  <circle cx="180" cy="60" r="4" fill="#d84315"/>
  
  <!-- FF Controller -->
  <line x1="180" y1="60" x2="240" y2="60" stroke="#d84315" stroke-width="2.5" marker-end="url(#arrow_ff)"/>
  <rect x="250" y="35" width="160" height="50" rx="6" fill="#fbe9e7" stroke="#d84315" stroke-width="2"/>
  <text x="330" y="60" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#bf360c" text-anchor="middle">G_ff(s) = -Gd/Gp</text>
  <text x="330" y="76" font-family="system-ui, sans-serif" font-size="9" fill="#666" text-anchor="middle">(Bù truyền thẳng)</text>
  
  <!-- Disturbance Gd -->
  <line x1="180" y1="60" x2="180" y2="195" stroke="#d84315" stroke-width="2"/>
  <line x1="180" y1="195" x2="510" y2="195" stroke="#d84315" stroke-width="2" marker-end="url(#arrow_ff)"/>
  <rect x="520" y="170" width="130" height="50" rx="6" fill="#fff3e0" stroke="#f57c00" stroke-width="1.5"/>
  <text x="585" y="200" font-family="system-ui, sans-serif" font-size="12" font-weight="bold" fill="#e65100" text-anchor="middle">G_d(s) (Kênh nhiễu)</text>
  
  <!-- Feedback loop -->
  <line x1="40" y1="125" x2="80" y2="125" stroke="#1565c0" stroke-width="2" marker-end="url(#arrow_fb)"/>
  <text x="60" y="115" font-family="sans-serif" font-size="10" font-weight="bold" fill="#1565c0" text-anchor="middle">SP (+)</text>
  <circle cx="95" cy="125" r="14" fill="#fff" stroke="#333" stroke-width="1.5"/>
  
  <line x1="109" y1="125" x2="140" y2="125" stroke="#1565c0" stroke-width="2" marker-end="url(#arrow_fb)"/>
  <rect x="150" y="100" width="120" height="50" rx="6" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="210" y="130" font-family="sans-serif" font-size="12" font-weight="bold" fill="#0d47a1" text-anchor="middle">C_fb(s) (PID)</text>
  
  <!-- Summing junction u_fb + u_ff -->
  <line x1="270" y1="125" x2="445" y2="125" stroke="#1565c0" stroke-width="2" marker-end="url(#arrow_fb)"/>
  <line x1="410" y1="60" x2="460" y2="60" stroke="#d84315" stroke-width="2"/>
  <line x1="460" y1="60" x2="460" y2="110" stroke="#d84315" stroke-width="2" marker-end="url(#arrow_ff)"/>
  
  <circle cx="460" cy="125" r="14" fill="#fff" stroke="#333" stroke-width="2"/>
  <text x="460" y="129" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">+</text>
  
  <line x1="474" y1="125" x2="510" y2="125" stroke="#1565c0" stroke-width="2" marker-end="url(#arrow_fb)"/>
  <rect x="520" y="100" width="130" height="50" rx="6" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="585" y="130" font-family="sans-serif" font-size="12" font-weight="bold" fill="#1b5e20" text-anchor="middle">G_p(s) (Plant)</text>
  
  <!-- Output Summing -->
  <line x1="650" y1="125" x2="695" y2="125" stroke="#1565c0" stroke-width="2" marker-end="url(#arrow_fb)"/>
  <line x1="650" y1="195" x2="710" y2="195" stroke="#d84315" stroke-width="2"/>
  <line x1="710" y1="195" x2="710" y2="140" stroke="#d84315" stroke-width="2" marker-end="url(#arrow_ff)"/>
  
  <circle cx="710" cy="125" r="14" fill="#fff" stroke="#333" stroke-width="2"/>
  <text x="710" y="129" font-family="sans-serif" font-size="14" font-weight="bold" text-anchor="middle">+</text>
  
  <line x1="724" y1="125" x2="780" y2="125" stroke="#1565c0" stroke-width="2.5" marker-end="url(#arrow_fb)"/>
  <text x="755" y="115" font-family="sans-serif" font-size="11" font-weight="bold" fill="#1565c0" text-anchor="middle">y(t) / PV</text>
</svg>"""

def get_htst_pid_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 230" width="100%" height="230">
  <defs>
    <marker id="arrow_pht" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#0277bd" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#fafafa" rx="8" stroke="#e0e0e0" stroke-width="1.5"/>
  <text x="400" y="24" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#333" text-anchor="middle">SƠ ĐỒ P&amp;ID THANH TRÙNG SỮA HTST (PLATE HEAT EXCHANGER + FDV)</text>
  
  <!-- Tank -->
  <rect x="30" y="65" width="70" height="95" rx="6" fill="#e0f7fa" stroke="#00838f" stroke-width="2"/>
  <text x="65" y="105" font-family="sans-serif" font-size="10" font-weight="bold" fill="#006064" text-anchor="middle">Bồn Sữa</text>
  <text x="65" y="120" font-family="sans-serif" font-size="10" font-weight="bold" fill="#006064" text-anchor="middle">Nguyên Liệu</text>
  
  <!-- Pump -->
  <line x1="100" y1="115" x2="150" y2="115" stroke="#0277bd" stroke-width="2.5" marker-end="url(#arrow_pht)"/>
  <circle cx="165" cy="115" r="14" fill="#fff" stroke="#0277bd" stroke-width="2"/>
  <text x="165" y="120" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0277bd" text-anchor="middle">P</text>
  
  <!-- Line into PHE -->
  <line x1="179" y1="115" x2="240" y2="115" stroke="#0277bd" stroke-width="2.5" marker-end="url(#arrow_pht)"/>
  
  <!-- PHE -->
  <rect x="250" y="55" width="120" height="115" rx="6" fill="#fff8e1" stroke="#fbc02d" stroke-width="2"/>
  <text x="310" y="90" font-family="sans-serif" font-size="12" font-weight="bold" fill="#f57f17" text-anchor="middle">Bộ PHE</text>
  <text x="310" y="108" font-family="sans-serif" font-size="10" fill="#555" text-anchor="middle">(Trao đổi nhiệt)</text>
  
  <line x1="310" y1="35" x2="310" y2="55" stroke="#d32f2f" stroke-width="2" marker-end="url(#arrow_pht)"/>
  <text x="350" y="44" font-family="sans-serif" font-size="9" font-weight="bold" fill="#d32f2f">Hơi nóng</text>
  
  <!-- Holding tube -->
  <line x1="370" y1="115" x2="430" y2="115" stroke="#0277bd" stroke-width="2.5"/>
  <rect x="430" y="100" width="110" height="30" rx="15" fill="#e1f5fe" stroke="#0288d1" stroke-width="2"/>
  <text x="485" y="120" font-family="sans-serif" font-size="10" font-weight="bold" fill="#01579b" text-anchor="middle">Ống lưu nhiệt θ</text>
  
  <!-- TT -->
  <line x1="540" y1="115" x2="580" y2="115" stroke="#0277bd" stroke-width="2"/>
  <circle cx="560" cy="75" r="14" fill="#fff" stroke="#d32f2f" stroke-width="1.5"/>
  <text x="560" y="80" font-family="sans-serif" font-size="10" font-weight="bold" fill="#d32f2f" text-anchor="middle">TT</text>
  <line x1="560" y1="89" x2="560" y2="115" stroke="#d32f2f" stroke-dasharray="2,2"/>
  
  <!-- FDV Valve -->
  <line x1="580" y1="115" x2="630" y2="115" stroke="#0277bd" stroke-width="2.5" marker-end="url(#arrow_pht)"/>
  <rect x="640" y="95" width="50" height="40" rx="4" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
  <text x="665" y="120" font-family="sans-serif" font-size="10" font-weight="bold" fill="#b71c1c" text-anchor="middle">FDV</text>
  
  <!-- Forward -->
  <line x1="690" y1="115" x2="770" y2="115" stroke="#2e7d32" stroke-width="2.5" marker-end="url(#arrow_pht)"/>
  <text x="735" y="105" font-family="sans-serif" font-size="9" font-weight="bold" fill="#2e7d32">T ≥ 72°C (Đạt)</text>
  
  <!-- Divert -->
  <line x1="665" y1="135" x2="665" y2="195" stroke="#c62828" stroke-width="2"/>
  <line x1="665" y1="195" x2="65" y2="195" stroke="#c62828" stroke-width="2"/>
  <line x1="65" y1="195" x2="65" y2="160" stroke="#c62828" stroke-width="2" marker-end="url(#arrow_pht)"/>
  <text x="365" y="212" font-family="sans-serif" font-size="10" font-weight="bold" fill="#c62828" text-anchor="middle">Dòng hồi lưu (Divert khi T &lt; 72°C để đảm bảo an toàn vi sinh)</text>
</svg>"""

def get_retort_pid_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 200" width="100%" height="200">
  <rect width="100%" height="100%" fill="#fafafa" rx="8" stroke="#e0e0e0" stroke-width="1.5"/>
  <text x="375" y="24" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#333" text-anchor="middle">SƠ ĐỒ P&amp;ID NỒI HẤP TIỆT TRÙNG RETORT (ĐỒ HỘP &amp; TÍNH F0 TÂM HỘP)</text>
  
  <!-- Retort Vessel -->
  <rect x="80" y="45" width="280" height="130" rx="20" fill="#ede7f6" stroke="#5e35b1" stroke-width="2.5"/>
  <text x="220" y="75" font-family="sans-serif" font-size="13" font-weight="bold" fill="#311b92" text-anchor="middle">Nồi Hấp Tiệt Trùng (Retort Vessel)</text>
  
  <!-- Cans inside -->
  <rect x="110" y="95" width="40" height="55" rx="4" fill="#cfd8dc" stroke="#455a64" stroke-width="1.5"/>
  <rect x="165" y="95" width="40" height="55" rx="4" fill="#cfd8dc" stroke="#455a64" stroke-width="1.5"/>
  <rect x="220" y="95" width="40" height="55" rx="4" fill="#ffe0b2" stroke="#e65100" stroke-width="2"/>
  <text x="240" y="125" font-family="sans-serif" font-size="9" font-weight="bold" fill="#e65100" text-anchor="middle">Hộp Đo</text>
  <rect x="275" y="95" width="40" height="55" rx="4" fill="#cfd8dc" stroke="#455a64" stroke-width="1.5"/>
  
  <!-- Thermocouple probe into core -->
  <circle cx="240" cy="120" r="3" fill="#d32f2f"/>
  <line x1="240" y1="120" x2="240" y2="45" stroke="#d32f2f" stroke-width="1.5" stroke-dasharray="2,2"/>
  <circle cx="240" cy="35" r="12" fill="#fff" stroke="#d32f2f" stroke-width="1.5"/>
  <text x="240" y="39" font-family="sans-serif" font-size="9" font-weight="bold" fill="#d32f2f" text-anchor="middle">TT_core</text>
  
  <!-- Calculations on the right -->
  <g transform="translate(400, 45)">
    <rect x="0" y="0" width="310" height="130" rx="6" fill="#fff" stroke="#b39ddb" stroke-width="1.5"/>
    <text x="155" y="25" font-family="sans-serif" font-size="12" font-weight="bold" fill="#512da8" text-anchor="middle">MÔ HÌNH NHIỆT ĐỘNG &amp; VI SINH</text>
    <text x="15" y="52" font-family="sans-serif" font-size="11" fill="#333">• <b>Quán tính hơi:</b> dT_vessel/dt = f(U_steam)</text>
    <text x="15" y="74" font-family="sans-serif" font-size="11" fill="#333">• <b>Truyền nhiệt tâm:</b> dT_core/dt = (T_vessel - T_core)/τ2</text>
    <text x="15" y="98" font-family="sans-serif" font-size="11" fill="#333">• <b>Giá trị tiệt trùng F0:</b> ∫ 10^((T_core - 121.1)/10) dt</text>
    <text x="15" y="118" font-family="sans-serif" font-size="10" font-weight="bold" fill="#c62828">🎯 Mục tiêu: F0 ≥ 3.0 min (tiêu diệt C. botulinum)</text>
  </g>
</svg>"""

def get_buffer_tank_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 750 200" width="100%" height="200">
  <defs>
    <marker id="arrow_tk" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 8 5 L 0 8.5 z" fill="#1565c0" />
    </marker>
  </defs>
  <rect width="100%" height="100%" fill="#fafafa" rx="8" stroke="#e0e0e0" stroke-width="1.5"/>
  <text x="375" y="24" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#333" text-anchor="middle">SƠ ĐỒ P&amp;ID ĐIỀU KHIỂN MỨC CHẤT LỎNG BỒN ĐỆM (BUFFER TANK)</text>
  
  <!-- Inflow -->
  <line x1="50" y1="55" x2="160" y2="55" stroke="#1565c0" stroke-width="2.5" marker-end="url(#arrow_tk)"/>
  <text x="105" y="45" font-family="sans-serif" font-size="10" font-weight="bold" fill="#1565c0" text-anchor="middle">Dòng nạp q_in(t)</text>
  
  <!-- Tank -->
  <rect x="170" y="50" width="140" height="120" rx="4" fill="#fff" stroke="#0277bd" stroke-width="2"/>
  <!-- Liquid in tank -->
  <rect x="172" y="100" width="136" height="68" fill="#b3e5fc" opacity="0.8"/>
  <text x="240" y="135" font-family="sans-serif" font-size="12" font-weight="bold" fill="#01579b" text-anchor="middle">Mức h(t)</text>
  <text x="240" y="155" font-family="sans-serif" font-size="10" fill="#555" text-anchor="middle">Diện tích đáy A</text>
  
  <!-- Level Transmitter LT & Controller LC -->
  <circle cx="350" cy="85" r="14" fill="#fff" stroke="#0277bd" stroke-width="1.5"/>
  <text x="350" y="90" font-family="sans-serif" font-size="10" font-weight="bold" fill="#0277bd" text-anchor="middle">LT</text>
  <line x1="310" y1="85" x2="336" y2="85" stroke="#0277bd" stroke-dasharray="2,2"/>
  
  <!-- Outflow -->
  <line x1="310" y1="160" x2="420" y2="160" stroke="#1565c0" stroke-width="2.5" marker-end="url(#arrow_tk)"/>
  <text x="380" y="150" font-family="sans-serif" font-size="10" font-weight="bold" fill="#1565c0">q_out = Cv·√h</text>
  
  <!-- Equations on the right -->
  <g transform="translate(460, 45)">
    <rect x="0" y="0" width="250" height="125" rx="6" fill="#fff" stroke="#90caf9" stroke-width="1.5"/>
    <text x="125" y="25" font-family="sans-serif" font-size="11" font-weight="bold" fill="#0d47a1" text-anchor="middle">PHƯƠNG TRÌNH ĐỘNG HỌC</text>
    <text x="15" y="55" font-family="sans-serif" font-size="11" fill="#333">• <b>Cân bằng:</b> A·dh/dt = q_in - q_out</text>
    <text x="15" y="80" font-family="sans-serif" font-size="11" fill="#333">• <b>Tuyến tính:</b> G(s) = R / (A·R·s + 1)</text>
    <text x="15" y="105" font-family="sans-serif" font-size="10" fill="#555">R: Điện trở thủy lực dòng xả</text>
  </g>
</svg>"""

print("All 9 SVG definitions generated and verified successfully!")
