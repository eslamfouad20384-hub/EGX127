import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import ta
import time
import re
import requests
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed

# =========================================================
# ⚙️ إعداد الصفحة
# =========================================================

st.set_page_config(
    page_title="EGX AI PRO MAX v10.3.1 - Portfolio Advisor",
    page_icon="📈",
    layout="wide"
)

st.title("🚀 EGX AI PRO MAX v10.3.1 | Trading & Investment + Portfolio Advisor")
st.caption(
    "📊 201 EGX stocks • Technical Engine • Sectoral Financial Engine • Portfolio Manager"
)

# =========================================================
# 📌 قائمة الأسهم
# =========================================================

EGX100 = [
    "COMI.CA", "MFPC.CA", "PHDC.CA", "ORAS.CA", "HDBK.CA", 
    "EFIH.CA", "AMES.CA", "INEG.CA",
    "BTFH.CA", "BIOC.CA",
    "CLHO.CA", "MBSC.CA",  
    "MTIE.CA", "EGTS.CA", "EGSA.CA", 
    "MHOT.CA", "EGBE.CA", "IFAP.CA", "PRDC.CA",
    "MIPH.CA", "MPCI.CA", "MOIN.CA", "ISMQ.CA",
    "AXPH.CA", "PHTV.CA", "CPCI.CA",
    "NINH.CA", "SPIN.CA", "ENGC.CA",
    "CNFN.CA", "SVCE.CA", "KABO.CA",
    "OFH.CA",  "GSSC.CA", "WCDF.CA", "MFSC.CA",
    "SAIB.CA", "ACGC.CA", "UEFM.CA", "KZPC.CA",
    "ADCI.CA", "INFI.CA", "ASCM.CA", 
    "ZEOT.CA", "SMFR.CA", "ETRS.CA", "CIRA.CA",
    "EDFM.CA", "MILS.CA", "GBCO.CA", "SCTS.CA",
    "HRHO.CA", "TMGH.CA", "FWRY.CA", "SWDY.CA", "ETEL.CA",
    "AMOC.CA", "HELI.CA", "EAST.CA", "EFID.CA", "JUFO.CA",
    "ABUK.CA", "EMFD.CA", "CCAP.CA",
    "CICH.CA", "OCDI.CA", "ORHD.CA", "MASR.CA",
    "ADIB.CA", "SAUD.CA", "CIEB.CA", "FAIT.CA", "AFDI.CA",
    "CANA.CA", "EXPA.CA", "ARCC.CA", "AJWA.CA", "MICH.CA",
    "SUGR.CA", "POUL.CA", "DOMT.CA", "ISMA.CA", "UEGC.CA",
    "FERC.CA", 
    "FAITA.CA",
"MAAL.CA",
"GGCC.CA",
"NDRL.CA",
"EFIC.CA",
"RTVC.CA",
"RUBX.CA",
"PRMH.CA",
"UNIP.CA",
"ICLE.CA",
"MEGM.CA",
"EASB.CA",
"APSW.CA",
"MOED.CA",
"KWIN.CA",
"RUBX.CA",
    "RMDA.CA",
    "OIH.CA",
    "SPHT.CA",
    "SDTI.CA",
    "GTWL.CA",
    "CFGH.CA",
    "NAHO.CA",
    "ACAMD.CA",
    "CEFM.CA",
    "ASPI.CA",
    "SCFM.CA",
    "CERA.CA",
    "DEIN.CA",
    "MBEG.CA",
    "SIPC.CA",
    "NHPS.CA",
    "ROTO.CA",
    "RAKT.CA",
    "EEII.CA",
    "CCRS.CA",
    "AREH.CA",
    "EPCO.CA",
    "GRCA.CA",
    "GIHD.CA",
    "ELWA.CA",
    "MMAT.CA",
    "NEDA.CA",
    "EPPK.CA",
    "GMCI.CA",
    "GPPL.CA", 
    "ADPC.CA",  
    "OBRI.CA",
    "RREI.CA",
    "RKAZ.CA",
    "SEIG.CA",
    "SNFC.CA",



"WKOL.CA",
"LUTS.CA",
"AIFI.CA",
"AMIA.CA",



"DTPP.CA",
"EALR.CA",
"EBSC.CA",
"EGREF.CA",
"EHDR.CA",
"ELNA.CA",
"EOSB.CA",
"FIRE.CA",
"FNAR.CA",


"ICID.CA",
"IDRE.CA",

"LCSW.CA",
"MOSC.CA",
    
    "OLFI.CA", "SKPC.CA", "AMER.CA", "TALM.CA", "ALUM.CA",
    "ORWE.CA", "SPMD.CA", "ZMID.CA", "MENA.CA", "DAPH.CA",
    "RAYA.CA", "EGAL.CA", "MPRC.CA", "AFMC.CA",
    "NCCW.CA", "SCEM.CA", "ARAB.CA", "GDWA.CA", "ELEC.CA",
    "IRON.CA", "ATQA.CA", "EGCH.CA", "ALCN.CA", "LCSW.CA",
    "MPCO.CA", "ELSH.CA", "MEPA.CA", "ODIN.CA", "EGAS.CA",
    "RACC.CA", "PRCL.CA", "BINV.CA", "MCQE.CA",
    "MOIL.CA", "NIPH.CA", "ISPH.CA", "DSCW.CA", "AALR.CA",
    "UNIT.CA", "PHAR.CA", "TRTO.CA", "CAED.CA", "CSAG.CA",
    "ICFC.CA", "ELKA.CA",
    "ATLC.CA", "COSG.CA", "AMPI.CA", "COPR.CA", "OCPH.CA",
]

EGX100 = list(dict.fromkeys(EGX100))
TOTAL_STOCKS = len(EGX100)

# =========================================================
# 🎛️ إعداداتl الفحص
# =========================================================

st.sidebar.header("⚙️ إعدادات الفحص")

period_daily = st.sidebar.selectbox(
    "📅 فترة البيانات اليومية",
    ["3mo", "6mo", "1y", "2y", "3y", "5y", "max"],
    index=6
)

period_weekly = st.sidebar.selectbox(
    "📅 فترة البيانات الأسبوعية",
    ["3y", "5y", "10y", "max"],
    index=3
)

period_monthly = st.sidebar.selectbox(
    "📅 فترة البيانات الشهرية",
    ["10y", "15y", "20y", "max"],
    index=3
)

max_workers = st.sidebar.slider(
    "⚡ عدد الاتصالات المتوازية",
    min_value=2,
    max_value=16,
    value=8,
    step=1
)

top_n = st.sidebar.slider(
    "🏆 عدد أفضل الأسهم",
    min_value=5,
    max_value=100,
    value=20,
    step=5
)

# =========================================================
# 💰 إدارة رأس المال
# =========================================================

st.sidebar.markdown("---")
st.sidebar.header("💰 إدارة المخاطر")

capital = st.sidebar.number_input(
    "رأس المال بالجنيه",
    min_value=1000.0,
    max_value=100000000.0,
    value=100000.0,
    step=5000.0
)

risk_percent = st.sidebar.slider(
    "مخاطرة الصفقة %",
    min_value=0.5,
    max_value=10.0,
    value=2.0,
    step=0.5
)

run_backtest = st.sidebar.checkbox(
    "🧪 تشغيل Backtest تاريخي حقيقي",
    value=True
)
backtest_bars = st.sidebar.slider(
    "عدد شموع الـ Backtest لكل سهم",
    min_value=100,
    max_value=1000,
    value=300,
    step=50
)

# تكاليف التنفيذ والقيود الواقعية
st.sidebar.markdown("---")
st.sidebar.header("🧾 واقعية التنفيذ")
commission_pct = st.sidebar.number_input(
    "عمولة التنفيذ لكل جانب %", min_value=0.0, max_value=2.0, value=0.15, step=0.01
)
slippage_pct = st.sidebar.number_input(
    "Slippage لكل جانب %", min_value=0.0, max_value=2.0, value=0.10, step=0.01
)
max_position_pct = st.sidebar.slider(
    "أقصى حجم مركز من رأس المال %", min_value=5, max_value=100, value=20, step=5
)
monte_carlo_runs = st.sidebar.slider(
    "عدد محاكاة Monte Carlo", min_value=100, max_value=2000, value=500, step=100
)

# =========================================================
# 🏦 إعدادات التحليل المالي والاستثمار
# =========================================================
st.sidebar.markdown("---")
st.sidebar.header("🏦 التحليل المالي والاستثمار")
run_financial_scan = st.sidebar.checkbox(
    "تشغيل التحليل المالي لكل الأسهم الـ201",
    value=True,
    help="يجلب البيانات المالية فقط من Yahoo Finance ثم StockAnalysis ثم Mubasher لاستكمال النواقص. لا يغيّر مصادر أو بيانات التحليل الفني."
)
financial_workers = st.sidebar.slider(
    "اتصالات التحليل المالي المتوازية",
    min_value=1, max_value=8, value=4, step=1
)
cost_of_equity_pct = st.sidebar.number_input(
    "تكلفة حقوق الملكية / معدل الخصم %",
    min_value=8.0, max_value=35.0, value=18.0, step=0.5
)
base_growth_pct = st.sidebar.number_input(
    "نمو التدفقات الأساسي المتوقع %",
    min_value=-10.0, max_value=30.0, value=5.0, step=1.0
)
terminal_growth_pct = st.sidebar.number_input(
    "النمو طويل الأجل Terminal Growth %",
    min_value=0.0, max_value=10.0, value=3.0, step=0.5
)
target_pe_multiple = st.sidebar.number_input(
    "معامل تعديل مضاعفات P/E القطاعية", min_value=4.0, max_value=25.0, value=10.0, step=0.5,
    help="10 = استخدام مضاعف كل قطاع كما هو محدد في محرك التقييم؛ الزيادة/النقصان تعدل جميع مضاعفات القطاعات نسبيًا."
)
if terminal_growth_pct >= cost_of_equity_pct:
    st.sidebar.warning("معدل النمو طويل الأجل لازم يكون أقل من معدل الخصم.")

# =========================================================
# 📊 معلومات
# =========================================================

st.sidebar.markdown("---")

st.sidebar.metric(
    "📊 عدد الأسهم للفحص",
    TOTAL_STOCKS
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    📌 النظام يقوم بفحص:

    • Daily / Weekly / Monthly
    • EMA20 / EMA50 / EMA200
    • RSI / MACD / ADX / ATR
    • OBV / MFI / Stochastic RSI / VWAP
    • Volume Ratio
    • Support / Resistance
    • Swing High / Swing Low
    • Fibonacci
    • Fibonacci Extensions
    • Professional Pullback
    • Professional Breakout
    • Trend Alignment
    • Entry Quality
    • Target Quality
    • Risk / Reward
    • Risk Management
    • 4 Targets
    • Backtest واقعي بتكاليف التنفيذ وSlippage
    • Strict Structural Targets فقط في Backtest
    • Partial Take Profit + Trailing Stop
    • Historical TP Probability / Expectancy
    • Walk-Forward / Out-of-Sample
    • Monte Carlo / Sharpe / Sortino / Calmar
    """
)

# =========================================================
# 🧠 ثوابت النظام
# =========================================================

MIN_DAILY_ROWS = 60
MIN_WEEKLY_ROWS = 80
MIN_MONTHLY_ROWS = 36

DOWNLOAD_RETRIES = 3
DOWNLOAD_RETRY_DELAY = 2

EMA200_REQUIRED_ROWS = 200

# Backtest / Structure / Liquidity
BACKTEST_WARMUP = 220
PIVOT_RADIUS = 3
LIQUIDITY_LOOKBACK = 20
RS_LOOKBACK = 20
DEFAULT_COMMISSION_PCT = 0.15
DEFAULT_SLIPPAGE_PCT = 0.10
DEFAULT_MAX_POSITION_PCT = 20.0

# =========================================================
# 📥 DATA ENGINE
# =========================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def load_data(symbols, period, interval):

    if not symbols:
        return pd.DataFrame()

    symbols = tuple(symbols)

    last_error = None

    for attempt in range(DOWNLOAD_RETRIES):

        try:

            data = yf.download(
                tickers=list(symbols),
                period=period,
                interval=interval,
                group_by="ticker",
                threads=True,
                auto_adjust=True,
                progress=False,
                timeout=30
            )

            if data is not None and not data.empty:
                return data

            last_error = "Yahoo returned empty data"

        except Exception as e:

            last_error = str(e)

        if attempt < DOWNLOAD_RETRIES - 1:

            time.sleep(
                DOWNLOAD_RETRY_DELAY *
                (attempt + 1)
            )

    return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def load_raw_close_data(symbols):
    """تحميل Close غير المعدل لاستخدامه في التقييم المالي فقط، دون تغيير محرك التحليل الفني."""
    if not symbols:
        return pd.DataFrame()
    try:
        data = yf.download(
            tickers=list(symbols), period="5d", interval="1d", group_by="ticker",
            threads=True, auto_adjust=False, progress=False, timeout=30
        )
        return data if data is not None and not data.empty else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


# =========================================================
# 🔍 استخراج بيانات السهم
# =========================================================

def extract_symbol_data(data, symbol):

    try:

        if data is None or data.empty:
            return pd.DataFrame()

        if isinstance(data.columns, pd.MultiIndex):

            level0 = data.columns.get_level_values(0)
            level1 = data.columns.get_level_values(1)

            if symbol in level0:

                df = data[symbol].copy()

            elif symbol in level1:

                df = data.xs(
                    symbol,
                    axis=1,
                    level=1
                ).copy()

            else:

                return pd.DataFrame()

        else:

            df = data.copy()

        df.columns = [
            str(c).strip()
            for c in df.columns
        ]

        required = [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]

        if not all(
            c in df.columns
            for c in required
        ):

            return pd.DataFrame()

        df = df[required].copy()

        for col in required:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        df = df.replace(
            [np.inf, -np.inf],
            np.nan
        )

        df = df.dropna(
            subset=[
                "Open",
                "High",
                "Low",
                "Close"
            ]
        )

        df["Volume"] = df["Volume"].fillna(0)

        df = df[
            (df["High"] >= df["Low"]) &
            (df["Close"] > 0) &
            (df["Open"] > 0)
        ]

        df = df.sort_index()

        df = df[
            ~df.index.duplicated(
                keep="last"
            )
        ]

        return df

    except Exception:

        return pd.DataFrame()


# =========================================================
# 🧪 DATA QUALITY
# =========================================================

def calculate_data_quality(df):

    if df is None or df.empty:

        return {
            "quality": 0.0,
            "missing": 100.0,
            "rows": 0
        }

    required = [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]

    total_cells = len(df) * len(required)

    missing_cells = int(
        df[required]
        .isna()
        .sum()
        .sum()
    )

    missing_pct = (
        missing_cells /
        total_cells *
        100
        if total_cells > 0
        else 100
    )

    quality = max(
        0.0,
        100.0 - missing_pct
    )

    if len(df) < 50:

        quality *= len(df) / 50

    return {
        "quality": round(
            quality,
            2
        ),
        "missing": round(
            missing_pct,
            2
        ),
        "rows": len(df)
    }


# =========================================================
# 📊 ATR
# =========================================================

def atr(df, period=14):

    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ],
        axis=1
    ).max(axis=1)

    return tr.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()


# =========================================================
# 📊 ADX
# =========================================================

def adx(df, period=14):

    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    plus_dm_raw = high.diff()
    minus_dm_raw = -low.diff()

    plus_dm = np.where(
        (plus_dm_raw > minus_dm_raw) &
        (plus_dm_raw > 0),
        plus_dm_raw,
        0.0
    )

    minus_dm = np.where(
        (minus_dm_raw > plus_dm_raw) &
        (minus_dm_raw > 0),
        minus_dm_raw,
        0.0
    )

    tr = pd.concat(
        [
            high - low,
            (high - close.shift()).abs(),
            (low - close.shift()).abs()
        ],
        axis=1
    ).max(axis=1)

    atr_val = tr.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()

    plus_di = (
        100 *
        pd.Series(
            plus_dm,
            index=df.index
        ).ewm(
            alpha=1 / period,
            adjust=False,
            min_periods=period
        ).mean()
        /
        (atr_val + 1e-9)
    )

    minus_di = (
        100 *
        pd.Series(
            minus_dm,
            index=df.index
        ).ewm(
            alpha=1 / period,
            adjust=False,
            min_periods=period
        ).mean()
        /
        (atr_val + 1e-9)
    )

    dx = (
        abs(
            plus_di -
            minus_di
        )
        /
        (
            plus_di +
            minus_di +
            1e-9
        )
    ) * 100

    return dx.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()


# =========================================================
# 📐 خطي Regression بسيط
# =========================================================

def linear_slope(series, window=10):

    if len(series) < window:
        return np.nan

    values = series.iloc[-window:].values.astype(float)

    if not np.all(np.isfinite(values)):
        return np.nan

    x = np.arange(window)

    try:

        slope = np.polyfit(
            x,
            values,
            1
        )[0]

        return float(slope)

    except Exception:

        return np.nan


# =========================================================
# 📈 TECHNICAL ENGINE
# =========================================================

def add_indicators(df):

    df = df.copy()

    if len(df) < 30:
        return df

    close = df["Close"]
    high = df["High"]
    low = df["Low"]
    vol = df["Volume"]

    # =====================================================
    # EMA20
    # =====================================================

    df["ema20"] = close.ewm(
        span=20,
        adjust=False
    ).mean()

    # =====================================================
    # EMA50
    # =====================================================

    df["ema50"] = close.ewm(
        span=50,
        adjust=False
    ).mean()

    # =====================================================
    # EMA200
    #
    # مهم:
    # لا نعتبر EMA200 مكتملًا إلا بعد 200 شمعة
    # =====================================================

    if len(df) >= EMA200_REQUIRED_ROWS:

        df["ema200"] = close.ewm(
            span=200,
            adjust=False,
            min_periods=200
        ).mean()

        df["ema200_complete"] = True

    else:

        df["ema200"] = np.nan
        df["ema200_complete"] = False

    # =====================================================
    # RSI
    # =====================================================

    df["rsi"] = ta.momentum.RSIIndicator(
        close=close,
        window=14
    ).rsi()

    # =====================================================
    # MACD
    # =====================================================

    macd_obj = ta.trend.MACD(
        close=close,
        window_slow=26,
        window_fast=12,
        window_sign=9
    )

    df["macd"] = macd_obj.macd()

    df["macd_signal"] = (
        macd_obj.macd_signal()
    )

    df["macd_hist"] = (
        macd_obj.macd_diff()
    )

    # =====================================================
    # Volume MA
    # =====================================================

    df["vol_ma"] = vol.rolling(
        20,
        min_periods=10
    ).mean()

    # =====================================================
    # Volume Ratio
    # =====================================================

    df["volume_ratio"] = (
        vol /
        (df["vol_ma"] + 1e-9)
    )

    # =====================================================
    # OBV
    # =====================================================

    try:

        df["obv"] = (
            ta.volume
            .OnBalanceVolumeIndicator(
                close=close,
                volume=vol
            )
            .on_balance_volume()
        )

        df["obv_ma"] = (
            df["obv"]
            .rolling(
                20,
                min_periods=10
            )
            .mean()
        )

        df["obv_slope"] = (
            df["obv"] -
            df["obv"].shift(5)
        )

    except Exception:

        df["obv"] = np.nan
        df["obv_ma"] = np.nan
        df["obv_slope"] = np.nan

    # =====================================================
    # MFI
    # =====================================================

    try:

        df["mfi"] = (
            ta.volume
            .MFIIndicator(
                high=high,
                low=low,
                close=close,
                volume=vol,
                window=14
            )
            .money_flow_index()
        )

    except Exception:

        df["mfi"] = np.nan

    # =====================================================
    # Stochastic RSI
    # =====================================================

    try:

        stoch = ta.momentum.StochRSIIndicator(
            close=close,
            window=14,
            smooth1=3,
            smooth2=3
        )

        df["stoch_rsi"] = (
            stoch.stochrsi()
        )

        df["stoch_rsi_k"] = (
            stoch.stochrsi_k()
        )

        df["stoch_rsi_d"] = (
            stoch.stochrsi_d()
        )

        df["stoch_rsi_k_slope"] = (
            df["stoch_rsi_k"] -
            df["stoch_rsi_k"].shift(1)
        )

    except Exception:

        df["stoch_rsi"] = np.nan
        df["stoch_rsi_k"] = np.nan
        df["stoch_rsi_d"] = np.nan
        df["stoch_rsi_k_slope"] = np.nan

    # =====================================================
    # VWAP
    # =====================================================

    try:

        typical_price = (
            high +
            low +
            close
        ) / 3

        cumulative_volume = vol.cumsum()

        df["vwap"] = (
            (
                typical_price *
                vol
            ).cumsum()
            /
            (
                cumulative_volume +
                1e-9
            )
        )

        df["vwap_distance"] = (
            close -
            df["vwap"]
        ) / (
            close +
            1e-9
        )

    except Exception:

        df["vwap"] = np.nan
        df["vwap_distance"] = np.nan

    # =====================================================
    # ATR
    # =====================================================

    df["atr"] = atr(
        df,
        14
    )

    df["atr_pct"] = (
        df["atr"] /
        (close + 1e-9)
    )

    # =====================================================
    # ADX
    # =====================================================

    df["adx"] = adx(
        df,
        14
    )

    # =====================================================
    # Support / Resistance
    # =====================================================

    df["support"] = (
        low
        .rolling(
            20,
            min_periods=10
        )
        .min()
    )

    df["resistance"] = (
        high
        .rolling(
            20,
            min_periods=10
        )
        .max()
    )

    # =====================================================
    # Previous Support / Resistance
    # =====================================================

    df["previous_support"] = (
        low
        .rolling(
            20,
            min_periods=10
        )
        .min()
        .shift(1)
    )

    df["previous_resistance"] = (
        high
        .rolling(
            20,
            min_periods=10
        )
        .max()
        .shift(1)
    )

    # =====================================================
    # Swing High / Swing Low
    #
    # نستخدم مستويات تاريخية حقيقية داخل النوافذ
    # =====================================================

    df["swing_high_20"] = (
        high
        .rolling(
            20,
            min_periods=10
        )
        .max()
        .shift(1)
    )

    df["swing_low_20"] = (
        low
        .rolling(
            20,
            min_periods=10
        )
        .min()
        .shift(1)
    )

    df["swing_high_60"] = (
        high
        .rolling(
            60,
            min_periods=20
        )
        .max()
        .shift(1)
    )

    df["swing_low_60"] = (
        low
        .rolling(
            60,
            min_periods=20
        )
        .min()
        .shift(1)
    )

    # =====================================================
    # Fibonacci
    # =====================================================

    swing_high = (
        high
        .rolling(
            60,
            min_periods=20
        )
        .max()
    )

    swing_low = (
        low
        .rolling(
            60,
            min_periods=20
        )
        .min()
    )

    fib_range = (
        swing_high -
        swing_low
    )

    df["fib_236"] = (
        swing_high -
        fib_range * 0.236
    )

    df["fib_382"] = (
        swing_high -
        fib_range * 0.382
    )

    df["fib_500"] = (
        swing_high -
        fib_range * 0.500
    )

    df["fib_618"] = (
        swing_high -
        fib_range * 0.618
    )

    df["fib_786"] = (
        swing_high -
        fib_range * 0.786
    )

    # =====================================================
    # Fibonacci Extensions
    # =====================================================

    df["fib_ext_1272"] = (
        swing_low +
        fib_range * 1.272
    )

    df["fib_ext_1618"] = (
        swing_low +
        fib_range * 1.618
    )

    df["fib_ext_2000"] = (
        swing_low +
        fib_range * 2.000
    )

    # =====================================================
    # Trend Slope
    # =====================================================

    df["ema20_slope"] = (
        df["ema20"] -
        df["ema20"].shift(5)
    ) / (
        df["Close"] + 1e-9
    )

    df["ema50_slope"] = (
        df["ema50"] -
        df["ema50"].shift(5)
    ) / (
        df["Close"] + 1e-9
    )

    # =====================================================
    # Candle Body
    # =====================================================

    candle_range = (
        high -
        low
    ).replace(
        0,
        np.nan
    )

    df["body_pct"] = (
        abs(
            close -
            df["Open"]
        ) /
        candle_range
    )

    df["bullish_candle"] = (
        close >
        df["Open"]
    )

    # =====================================================
    # ATR مناسب للاختراق
    # =====================================================

    df["atr_expansion"] = (
        df["atr"] /
        (
            df["atr"]
            .rolling(
                20,
                min_periods=10
            )
            .mean()
            +
            1e-9
        )
    )

    # =====================================================
    # Breakout متقدم
    # =====================================================

    previous_resistance = (
        high
        .rolling(
            20,
            min_periods=10
        )
        .max()
        .shift(1)
    )

    close_above_resistance = (
        close >
        previous_resistance
    )

    breakout_volume = (
        df["volume_ratio"] >= 1.30
    )

    breakout_volume_strong = (
        df["volume_ratio"] >= 1.50
    )

    atr_is_healthy = (
        df["atr_pct"] >= 0.015
    )

    atr_not_extreme = (
        df["atr_pct"] <= 0.12
    )

    candle_quality = (
        df["body_pct"] >= 0.45
    )

    bullish_candle = (
        df["bullish_candle"]
    )

    trend_breakout = (
        (
            close > df["ema20"]
        ) &
        (
            df["ema20"] > df["ema50"]
        )
    )

    df["breakout"] = (
        close_above_resistance &
        breakout_volume &
        atr_is_healthy &
        atr_not_extreme &
        candle_quality &
        bullish_candle &
        trend_breakout
    )

    # =====================================================
    # Pullback متقدم
    # =====================================================

    distance_ema20 = (
        abs(
            close -
            df["ema20"]
        ) /
        (close + 1e-9)
    )

    distance_ema50 = (
        abs(
            close -
            df["ema50"]
        ) /
        (close + 1e-9)
    )

    near_ema20 = (
        distance_ema20 <= 0.025
    )

    near_ema50 = (
        distance_ema50 <= 0.035
    )

    trend_bullish = (
        (close > df["ema50"]) &
        (df["ema20"] > df["ema50"]) &
        (df["ema20_slope"] > 0)
    )

    support_near = (
        (
            abs(
                close -
                df["previous_support"]
            ) /
            (close + 1e-9)
        ) <= 0.04
    )

    fib_support_near = (
        (
            (
                abs(close - df["fib_382"]) /
                (close + 1e-9)
            ) <= 0.025
        )
        |
        (
            (
                abs(close - df["fib_500"]) /
                (close + 1e-9)
            ) <= 0.025
        )
        |
        (
            (
                abs(close - df["fib_618"]) /
                (close + 1e-9)
            ) <= 0.025
        )
    )

    # انخفاض ضغط البيع:
    # حجم البيع الحالي ليس أعلى بشكل حاد
    # والسهم لا يغلق بالقرب من قاع الشمعة
    close_location = (
        close -
        low
    ) / (
        candle_range +
        1e-9
    )

    selling_pressure_reduced = (
        (
            df["volume_ratio"] <= 1.30
        ) &
        (
            close_location >= 0.45
        )
    )

    bullish_confirmation = (
        (
            bullish_candle &
            (
                body := df["body_pct"]
            ).ge(0.35)
        )
        |
        (
            close >
            df["ema20"]
        )
    )

    pullback_score = (
        trend_bullish.astype(int) * 2 +
        (
            near_ema20 |
            near_ema50
        ).astype(int) * 2 +
        support_near.astype(int) +
        fib_support_near.astype(int) +
        selling_pressure_reduced.astype(int) +
        bullish_confirmation.astype(int)
    )

    df["pullback_quality_score"] = (
        pullback_score
    )

    df["pullback"] = (
        (
            pullback_score >= 6
        ) &
        trend_bullish
    )

    # =====================================================
    # Confirmed Swing Engine - no look-ahead at decision time
    # Pivot is only considered confirmed after PIVOT_RADIUS candles
    # =====================================================
    w = PIVOT_RADIUS * 2 + 1
    ph_candidate = high.eq(high.rolling(w, center=True, min_periods=w).max())
    pl_candidate = low.eq(low.rolling(w, center=True, min_periods=w).min())

    df["confirmed_swing_high_raw"] = high.where(ph_candidate).shift(PIVOT_RADIUS)
    df["confirmed_swing_low_raw"] = low.where(pl_candidate).shift(PIVOT_RADIUS)
    df["confirmed_swing_high"] = df["confirmed_swing_high_raw"].ffill()
    df["confirmed_swing_low"] = df["confirmed_swing_low_raw"].ffill()

    # Last confirmed pivot timestamps, also shifted by confirmation delay.
    idx_num = pd.Series(np.arange(len(df), dtype=float), index=df.index)
    df["confirmed_high_idx"] = idx_num.where(ph_candidate).shift(PIVOT_RADIUS).ffill()
    df["confirmed_low_idx"] = idx_num.where(pl_candidate).shift(PIVOT_RADIUS).ffill()

    # =====================================================
    # Confirmed Fibonacci - based on the latest confirmed impulse
    # =====================================================
    bull_leg = (
        df["confirmed_low_idx"].notna() &
        df["confirmed_high_idx"].notna() &
        (df["confirmed_low_idx"] < df["confirmed_high_idx"])
    )
    fib_hi = df["confirmed_swing_high"]
    fib_lo = df["confirmed_swing_low"]
    fib_range_confirmed = (fib_hi - fib_lo).where(bull_leg)

    for ratio, col in [(0.236, "fib_236"), (0.382, "fib_382"), (0.500, "fib_500"), (0.618, "fib_618"), (0.786, "fib_786")]:
        df[col] = (fib_hi - fib_range_confirmed * ratio).where(fib_range_confirmed > 0)

    # Bullish extensions are measured from confirmed low -> confirmed high.
    df["fib_ext_1272"] = (fib_hi + fib_range_confirmed * 0.272).where(fib_range_confirmed > 0)
    df["fib_ext_1618"] = (fib_hi + fib_range_confirmed * 0.618).where(fib_range_confirmed > 0)
    df["fib_ext_2000"] = (fib_hi + fib_range_confirmed * 1.000).where(fib_range_confirmed > 0)

    # =====================================================
    # Liquidity Engine: EGP turnover, not raw share volume
    # =====================================================
    df["turnover"] = close * vol
    df["turnover_ma20"] = df["turnover"].rolling(LIQUIDITY_LOOKBACK, min_periods=10).median()
    df["liquidity_ratio"] = df["turnover"] / (df["turnover_ma20"] + 1e-9)

    # Relative strength is computed later against the EGX cross-sectional proxy.
    df["return_20d"] = close.pct_change(RS_LOOKBACK)

    return df


# =========================================================
# 🧠 MARKET REGIME
# =========================================================

def market_regime(last):

    score = 0

    checks = [
        (
            np.isfinite(last.get("ema200", np.nan)) and
            last["Close"] > last["ema200"]
        ),
        last["ema20"] > last["ema50"],
        (
            np.isfinite(last.get("ema200", np.nan)) and
            last["ema50"] > last["ema200"]
        ),
        last["macd"] > last["macd_signal"],
        last["rsi"] > 50,
        last["adx"] > 20
    ]

    score = sum(checks)

    if score >= 6:
        return "🚀 قوي جداً"

    elif score >= 4:
        return "🟢 صعود"

    elif score >= 3:
        return "🟡 محايد"

    else:
        return "🔴 هبوط"


# =========================================================
# 📊 TIMEFRAME SCORE
# =========================================================

def timeframe_score(df):

    if df is None or df.empty:
        return 0

    last = df.iloc[-1]

    score = 0

    if (
        np.isfinite(last.get("ema200", np.nan)) and
        last["Close"] > last["ema200"]
    ):
        score += 25

    if last["ema20"] > last["ema50"]:
        score += 20

    if (
        np.isfinite(last.get("ema200", np.nan)) and
        last["ema50"] > last["ema200"]
    ):
        score += 20

    if last["macd"] > last["macd_signal"]:
        score += 15

    if last["rsi"] > 50:
        score += 10

    if last["ema20_slope"] > 0:
        score += 10

    # لا نعطي Score EMA200 كامل إذا غير مكتمل
    if not bool(last.get("ema200_complete", False)):
        score = min(
            score,
            55
        )

    return score


# =========================================================
# 📊 TREND ALIGNMENT
# =========================================================

def trend_alignment_score(
    df_d,
    df_w,
    df_m
):

    daily_score = timeframe_score(
        df_d
    )

    weekly_score = timeframe_score(
        df_w
    )

    monthly_score = timeframe_score(
        df_m
    )

    alignment = (
        daily_score * 0.40 +
        weekly_score * 0.35 +
        monthly_score * 0.25
    )

    return min(
        100,
        max(
            0,
            alignment
        )
    )


# =========================================================
# 🎯 حساب Pullback Entry
# =========================================================

def calculate_pullback_entry(df_d):
    last = df_d.iloc[-1]
    close = float(last["Close"])
    atr_val = float(last.get("atr", close * 0.03))
    if not np.isfinite(atr_val) or atr_val <= 0:
        atr_val = close * 0.03

    levels = []
    candidates = [
        ("Confirmed Support", last.get("previous_support", np.nan)),
        ("Confirmed Swing Low", last.get("confirmed_swing_low", np.nan)),
        ("EMA20", last.get("ema20", np.nan)),
        ("EMA50", last.get("ema50", np.nan)),
        ("Fib 38.2%", last.get("fib_382", np.nan)),
        ("Fib 50%", last.get("fib_500", np.nan)),
        ("Fib 61.8%", last.get("fib_618", np.nan)),
    ]
    for name, level in candidates:
        try:
            level = float(level)
            if np.isfinite(level) and level > 0 and level <= close:
                levels.append((name, level))
        except Exception:
            pass

    if not levels:
        return close, "لا توجد منطقة Pullback مؤكدة أسفل السعر"

    max_distance = max(atr_val * 1.5, close * 0.06)
    nearby = [x for x in levels if close - x[1] <= max_distance]
    if not nearby:
        return close, "لا يوجد Pullback قريب بما يكفي؛ انتظار تأكيد سعري"

    # Prefer the strongest structural level when several levels are close.
    priority = {"Confirmed Support": 1, "Confirmed Swing Low": 2, "Fib 61.8%": 3, "Fib 50%": 4, "Fib 38.2%": 5, "EMA50": 6, "EMA20": 7}
    name, price = min(nearby, key=lambda x: (priority.get(x[0], 99), abs(close-x[1])))
    return float(price), f"منطقة {name} مؤكدة + مسافة Pullback ضمن {max_distance/close*100:.1f}%"



# =========================================================
# 🎯 Entry Engine
# =========================================================

def determine_entry(
    df_d,
    alignment
):

    last = df_d.iloc[-1]

    market_price = float(
        last["Close"]
    )

    previous_resistance = float(
        last.get(
            "previous_resistance",
            np.nan
        )
    )

    ema20 = float(
        last["ema20"]
    )

    ema50 = float(
        last["ema50"]
    )

    breakout = bool(
        last.get(
            "breakout",
            False
        )
    )

    pullback = bool(
        last.get(
            "pullback",
            False
        )
    )

    volume_ratio = float(
        last["volume_ratio"]
    )

    atr_pct = float(
        last["atr_pct"]
    )

    body_pct = float(
        last.get(
            "body_pct",
            0
        )
    )

    # =====================================================
    # 1️⃣ Breakout
    # =====================================================

    if (
        breakout and
        np.isfinite(previous_resistance) and
        market_price > previous_resistance and
        volume_ratio >= 1.5 and
        0.015 <= atr_pct <= 0.12 and
        body_pct >= 0.45 and
        alignment >= 60
    ):

        return {
            "type": "دخول اختراق",
            "price": market_price,
            "reason": (
                "اختراق مقاومة سابقة + حجم قوي + "
                "شمعة اختراق جيدة + ATR مناسب + "
                "Trend Alignment قوي"
            )
        }

    # =====================================================
    # 2️⃣ Professional Pullback
    # =====================================================

    if (
        pullback and
        ema20 > ema50 and
        alignment >= 55
    ):

        pullback_price, pullback_reason = (
            calculate_pullback_entry(
                df_d
            )
        )

        return {
            "type": "دخول عند Pullback",
            "price": pullback_price,
            "reason": (
                "اتجاه صاعد + منطقة دعم/EMA/Fibonacci + "
                "انخفاض ضغط البيع + تأكيد سعري | "
                + pullback_reason
            )
        }

    # =====================================================
    # 3️⃣ Immediate
    # =====================================================

    if (
        market_price > ema20 and
        market_price > ema50 and
        last["rsi"] >= 50 and
        last["macd"] > last["macd_signal"] and
        market_price > last["vwap"] and
        volume_ratio >= 1.0 and
        alignment >= 50
    ):

        return {
            "type": "دخول فوري",
            "price": market_price,
            "reason": (
                "السعر فوق EMA20/50 وVWAP + "
                "RSI إيجابي + MACD إيجابي + "
                "حجم مقبول + Trend Alignment"
            )
        }

    # =====================================================
    # 4️⃣ Confirmation
    # =====================================================

    return {
        "type": "انتظار تأكيد",
        "price": market_price,
        "reason": (
            "لا توجد حاليًا شروط كافية "
            "لدخول اختراق أو Pullback أو دخول فوري"
        )
    }


# =========================================================
# 🎯 TARGET ENGINE HELPERS
# =========================================================

def add_target_level(
    levels,
    price,
    reason,
    category
):

    try:

        price = float(price)

        if (
            np.isfinite(price) and
            price > 0
        ):

            levels.append({
                "price": price,
                "reason": reason,
                "category": category
            })

    except Exception:
        pass


def deduplicate_levels(
    levels,
    tolerance
):

    if not levels:
        return []

    levels = sorted(
        levels,
        key=lambda x: x["price"]
    )

    result = []

    for level in levels:

        if not result:

            result.append(level)

        else:

            previous = result[-1]

            relative_gap = (
                abs(
                    level["price"] -
                    previous["price"]
                )
                /
                max(
                    previous["price"],
                    1e-9
                )
            )

            if relative_gap >= tolerance:

                result.append(level)

            else:

                # نحتفظ بالأعلى أولوية
                priority = {
                    "Resistance": 1,
                    "Swing High": 2,
                    "Weekly": 3,
                    "Monthly": 4,
                    "Fibonacci": 5,
                    "ATR": 6
                }

                old_priority = priority.get(
                    previous["category"],
                    99
                )

                new_priority = priority.get(
                    level["category"],
                    99
                )

                if new_priority < old_priority:

                    result[-1] = level

    return result


# =========================================================
# 🛡️ PROFESSIONAL RISK & TARGET ENGINE
# =========================================================

def calculate_risk_engine(df_d, entry, capital, risk_percent, df_w=None, df_m=None):
    last = df_d.iloc[-1]
    support = float(last.get("previous_support", np.nan))
    atr_val = float(last.get("atr", np.nan))
    if not np.isfinite(atr_val) or atr_val <= 0:
        atr_val = entry * 0.03

    bullish = bool(last.get("ema20", entry) > last.get("ema50", entry))
    # Stop is structural first, ATR only protects when no valid structure exists.
    stop_candidates = []
    for level in [support, last.get("confirmed_swing_low", np.nan)]:
        try:
            level = float(level)
            if np.isfinite(level) and 0 < level < entry:
                stop_candidates.append(level - atr_val * 0.20)
        except Exception:
            pass
    stop_candidates.append(entry - atr_val * (1.5 if bullish else 1.2))
    stop_candidates = [x for x in stop_candidates if np.isfinite(x) and 0 < x < entry]
    stop = max(stop_candidates) if stop_candidates else entry * 0.95

    risk_per_share = entry - stop
    if risk_per_share <= 0 or not np.isfinite(risk_per_share):
        risk_per_share = entry * 0.03
        stop = entry - risk_per_share
    risk_pct_actual = risk_per_share / entry
    allowed_loss = capital * risk_percent / 100.0
    position_size = allowed_loss / risk_per_share
    # V9: position-size cap prevents a mathematically valid but practically
    # oversized position when the stop is tight.
    max_position_value = capital * (DEFAULT_MAX_POSITION_PCT / 100.0)
    position_size = min(position_size, max_position_value / entry)
    position_value = position_size * entry

    # =====================================================
    # Target Engine: STRUCTURAL ONLY. No ATR-generated/fake targets.
    # =====================================================
    levels = []
    def add(price, reason, category):
        try:
            price = float(price)
            if np.isfinite(price) and price > entry:
                levels.append({"price": price, "reason": reason, "category": category})
        except Exception:
            pass

    add(last.get("previous_resistance", np.nan), "المقاومة اليومية السابقة", "Resistance")
    add(last.get("resistance", np.nan), "المقاومة اليومية الحالية", "Resistance")
    add(last.get("confirmed_swing_high", np.nan), "آخر Swing High مؤكد", "Swing High")

    for col, reason, cat in [
        ("fib_ext_1272", "Fibonacci Extension 127.2% مبني على Swing مؤكد", "Fibonacci"),
        ("fib_ext_1618", "Fibonacci Extension 161.8% مبني على Swing مؤكد", "Fibonacci"),
        ("fib_ext_2000", "Fibonacci Extension 200% مبني على Swing مؤكد", "Fibonacci"),
    ]:
        add(last.get(col, np.nan), reason, cat)

    if df_w is not None and not df_w.empty:
        try:
            w_high = df_w["High"].rolling(20, min_periods=10).max().shift(1).iloc[-1]
            add(w_high, "مقاومة Weekly سابقة", "Weekly")
        except Exception:
            pass
    if df_m is not None and not df_m.empty:
        try:
            m_high = df_m["High"].rolling(12, min_periods=6).max().shift(1).iloc[-1]
            add(m_high, "مقاومة Monthly سابقة", "Monthly")
        except Exception:
            pass

    priority = {"Resistance":1, "Swing High":2, "Weekly":3, "Monthly":4, "Fibonacci":5}
    levels.sort(key=lambda x: x["price"])
    dedup=[]
    for x in levels:
        if not dedup or abs(x["price"]-dedup[-1]["price"])/max(dedup[-1]["price"],1e-9) >= 0.008:
            dedup.append(x)
        elif priority.get(x["category"],99) < priority.get(dedup[-1]["category"],99):
            dedup[-1]=x

    min_gap = max(atr_val * 0.40, entry * 0.012)
    selected=[]
    for x in dedup:
        if not selected or x["price"] >= selected[-1]["price"] + min_gap:
            selected.append(x)
        if len(selected) >= 4:
            break

    # Do NOT fabricate missing targets.
    while len(selected) < 4:
        selected.append({"price": np.nan, "reason": "لا يوجد مستوى سعري هيكلي موثوق كافٍ", "category": "غير متاح"})

    prices=[x["price"] for x in selected]
    profits=[((p-entry)/entry*100) if np.isfinite(p) else np.nan for p in prices]
    rr=[((p-entry)/risk_per_share) if np.isfinite(p) else np.nan for p in prices]
    points={"Resistance":1.0,"Swing High":0.95,"Weekly":0.9,"Monthly":0.9,"Fibonacci":0.8,"غير متاح":0.0}
    target_quality=float(np.mean([points.get(x["category"],0.0) for x in selected])*100)

    structural_count=sum(np.isfinite(prices))
    return {
        "entry": float(entry), "stop": float(stop),
        "tp1": float(prices[0]) if np.isfinite(prices[0]) else np.nan,
        "tp2": float(prices[1]) if np.isfinite(prices[1]) else np.nan,
        "tp3": float(prices[2]) if np.isfinite(prices[2]) else np.nan,
        "tp4": float(prices[3]) if np.isfinite(prices[3]) else np.nan,
        "tp1_profit_pct": float(profits[0]) if np.isfinite(profits[0]) else np.nan,
        "tp2_profit_pct": float(profits[1]) if np.isfinite(profits[1]) else np.nan,
        "tp3_profit_pct": float(profits[2]) if np.isfinite(profits[2]) else np.nan,
        "tp4_profit_pct": float(profits[3]) if np.isfinite(profits[3]) else np.nan,
        "tp1_reason": selected[0]["reason"], "tp2_reason": selected[1]["reason"], "tp3_reason": selected[2]["reason"], "tp4_reason": selected[3]["reason"],
        "tp1_category": selected[0]["category"], "tp2_category": selected[1]["category"], "tp3_category": selected[2]["category"], "tp4_category": selected[3]["category"],
        "rr1": float(rr[0]) if np.isfinite(rr[0]) else np.nan, "rr2": float(rr[1]) if np.isfinite(rr[1]) else np.nan, "rr3": float(rr[2]) if np.isfinite(rr[2]) else np.nan, "rr4": float(rr[3]) if np.isfinite(rr[3]) else np.nan,
        "target_quality": target_quality, "risk_pct": float(risk_pct_actual*100),
        "position_size": float(position_size), "position_value": float(position_value),
        "structural_target_count": structural_count
    }



# =========================================================
# 🧠 CONFIDENCE ENGINE
# =========================================================

def ai_confidence(
    last_d,
    last_w,
    last_m,
    alignment,
    data_quality
):

    score = 0
    total = 13

    if (
        np.isfinite(last_d.get("ema200", np.nan)) and
        last_d["Close"] > last_d["ema200"]
    ):
        score += 1

    if (
        np.isfinite(last_w.get("ema200", np.nan)) and
        last_w["Close"] > last_w["ema200"]
    ):
        score += 1

    if (
        np.isfinite(last_m.get("ema200", np.nan)) and
        last_m["Close"] > last_m["ema200"]
    ):
        score += 1

    if last_d["macd"] > last_d["macd_signal"]:
        score += 1

    if 45 < last_d["rsi"] < 70:
        score += 1

    if last_d["volume_ratio"] > 1:
        score += 1

    if last_d["adx"] > 20:
        score += 1

    if 40 < last_d["mfi"] < 80:
        score += 1

    if (
        np.isfinite(last_d["obv"]) and
        np.isfinite(last_d["obv_ma"]) and
        last_d["obv"] > last_d["obv_ma"]
    ):
        score += 1

    if (
        np.isfinite(last_d["stoch_rsi_k"]) and
        np.isfinite(last_d["stoch_rsi_d"]) and
        last_d["stoch_rsi_k"] >
        last_d["stoch_rsi_d"]
    ):
        score += 1

    if (
        np.isfinite(last_d["vwap"]) and
        last_d["Close"] > last_d["vwap"]
    ):
        score += 1

    if alignment >= 60:
        score += 1

    if data_quality >= 90:
        score += 1

    return score / total


# =========================================================
# 🧠 CONFIDENCE TARGET MODEL
# =========================================================

def estimate_probabilities(
    base_conf,
    rr1,
    rr2,
    rr3,
    rr4,
    alignment,
    adx_val
):

    trend_factor = (
        alignment /
        100
    )

    momentum_factor = min(
        1.0,
        max(
            0.5,
            adx_val / 35
        )
    )

    base = (
        base_conf * 0.60 +
        trend_factor * 0.25 +
        momentum_factor * 0.15
    )

    tp1 = base

    if rr1 >= 2:
        tp1 += 0.05

    elif rr1 < 1.2:
        tp1 -= 0.10

    tp1 = min(
        0.90,
        max(
            0.20,
            tp1
        )
    )

    tp2 = tp1 * 0.82

    if rr2 >= 2:
        tp2 += 0.03

    elif rr2 < 1.5:
        tp2 -= 0.05

    tp2 = min(
        0.82,
        max(
            0.15,
            tp2
        )
    )

    tp3 = tp2 * 0.78

    if rr3 >= 2.5:
        tp3 += 0.03

    elif rr3 < 2:
        tp3 -= 0.05

    tp3 = min(
        0.75,
        max(
            0.10,
            tp3
        )
    )

    tp4 = tp3 * 0.72

    if rr4 >= 3:
        tp4 += 0.03

    elif rr4 < 2.5:
        tp4 -= 0.05

    tp4 = min(
        0.68,
        max(
            0.08,
            tp4
        )
    )

    return (
        tp1,
        tp2,
        tp3,
        tp4
    )



# =========================================================
# 🟢 نسبة الشراء الفنية — للعرض فقط
# لا تدخل في التقييم أو ترتيب الأسهم أو Entry/Risk/Targets.
# =========================================================
def calculate_buy_percentage(last_d, last_w, last_m, alignment, relative_strength):
    """
    مؤشر عرضي من 0-100 لقياس ميل الإشارات الفنية ناحية الشراء.
    لا يغيّر أي منطق تداول قائم في V9.
    """
    buy = 0.0
    total = 0.0

    def add(condition, weight):
        nonlocal buy, total
        total += float(weight)
        if bool(condition):
            buy += float(weight)

    # الاتجاه — Daily / Weekly / Monthly
    add(last_d["ema20"] > last_d["ema50"], 10)
    add(last_d["Close"] > last_d["ema50"], 5)
    add(last_w["ema20"] > last_w["ema50"], 5)
    add(last_m["ema20"] > last_m["ema50"], 5)

    # الزخم
    rsi = float(last_d.get("rsi", np.nan))
    if np.isfinite(rsi):
        if 50 <= rsi <= 65:
            buy += 7
        elif 45 <= rsi < 50 or 65 < rsi <= 70:
            buy += 5
        elif rsi >= 70:
            buy += 3
        total += 7

    add(
        float(last_d.get("macd", np.nan)) > float(last_d.get("macd_signal", np.nan)),
        8
    )

    add(
        float(last_d.get("stoch_rsi_k", np.nan)) >
        float(last_d.get("stoch_rsi_d", np.nan)),
        5
    )

    # السيولة / تدفق الأموال
    add(float(last_d.get("volume_ratio", np.nan)) >= 1.0, 5)
    add(
        50 <= float(last_d.get("mfi", np.nan)) <= 75,
        5
    )
    add(
        float(last_d.get("obv", np.nan)) > float(last_d.get("obv_ma", np.nan)),
        5
    )

    # السعر والاتجاه
    add(
        float(last_d.get("Close", np.nan)) >
        float(last_d.get("vwap", np.nan)),
        5
    )
    add(
        float(last_d.get("ema20_slope", np.nan)) > 0,
        5
    )

    # قوة الاتجاه العام
    add(float(alignment) >= 60, 10)

    # قوة السهم مقابل السوق
    try:
        rs = float(relative_strength)
    except Exception:
        rs = 0.0
    add(rs >= 0, 10)

    if total <= 0:
        return 50.0

    return round(float(np.clip(buy / total * 100.0, 0.0, 100.0)), 1)


def style_buy_percentage(value):
    """تنسيق بصري للخلية فقط: أخضر/أصفر/أحمر."""
    try:
        x = float(value)
    except Exception:
        return ""
    if x >= 60:
        return "background-color: rgba(0, 180, 0, 0.18); color: #0a7a0a; font-weight: 700;"
    if x < 40:
        return "background-color: rgba(220, 0, 0, 0.15); color: #b00000; font-weight: 700;"
    return "background-color: rgba(220, 170, 0, 0.16); color: #8a6a00; font-weight: 700;"

def display_with_buy_percentage(df):
    """عرض الجدول مع تلوين عمود نسبة الشراء فقط."""
    if "نسبة الشراء %" not in df.columns:
        return df
    return df.style.map(style_buy_percentage, subset=["نسبة الشراء %"])


# =========================================================
# 🏦 FINANCIAL INTELLIGENCE ENGINE
# =========================================================

def _empty_financial_snapshot():
    return {
        "income": pd.DataFrame(), "balance": pd.DataFrame(), "cashflow": pd.DataFrame(),
        "info": {}, "dividends": pd.Series(dtype=float), "source": "",
        "source_details": [], "field_sources": {}, "error": ""
    }


def _stockanalysis_number(value, amount_in_millions=True):
    """تحويل أرقام StockAnalysis؛ القوائم معروضة بملايين الجنيهات، وEPS لا يُضرب في مليون."""
    if value is None:
        return np.nan
    raw = str(value).strip().replace(',', '').replace('−', '-')
    if raw in ('', '-', '—', 'n/a', 'N/A', 'None'):
        return np.nan
    multiplier = 1.0
    if raw.endswith('%'):
        raw = raw[:-1]
    elif raw[-1:].upper() in ('B', 'M', 'K'):
        suffix = raw[-1].upper()
        raw = raw[:-1]
        multiplier = {'B': 1e9, 'M': 1e6, 'K': 1e3}[suffix]
    try:
        number = float(raw.replace('(', '-').replace(')', '')) * multiplier
        return number * 1e6 if amount_in_millions and multiplier == 1.0 else number
    except Exception:
        return np.nan


def _stockanalysis_statement_page(ticker, page):
    url = f"https://stockanalysis.com/quote/egx/{ticker}/financials/{page}"
    headers = {"User-Agent": "Mozilla/5.0 (compatible; EGXFinancialResearch/1.0)"}
    response = requests.get(url, headers=headers, timeout=14)
    response.raise_for_status()
    tables = pd.read_html(StringIO(response.text))
    rows = {}
    period_cols = []
    for table in tables:
        if table.empty:
            continue
        # الجدول غالبًا يحتوي عمود بند ثم TTM وFY 2025...
        first_col = table.iloc[:, 0].astype(str).str.strip()
        headers_text = [str(c) for c in table.columns]
        for _, row in table.iterrows():
            label = str(row.iloc[0]).strip()
            if not label or label.lower() in ('nan', 'none'):
                continue
            vals = {}
            for j in range(1, len(row)):
                col = headers_text[j] if j < len(headers_text) else f"col{j}"
                m = re.search(r'(?:FY\s*)?(20\d{2})', col)
                if m:
                    vals[int(m.group(1))] = row.iloc[j]
            if vals:
                rows[label.lower()] = (label, vals)
    return rows


def _stockanalysis_snapshot(symbol):
    ticker = symbol.replace('.CA', '').upper()
    result = _empty_financial_snapshot()
    result['source'] = 'StockAnalysis (S&P Global Market Intelligence)'
    result['source_details'].append('StockAnalysis')
    try:
        # صفحة النظرة المالية الواحدة تجمع الإيرادات والأرباح والتدفقات النقدية؛
        # نكتفي بطلب واحد لكل سهم لتقليل زمن فحص قائمة EGX كاملة.
        overview_rows = _stockanalysis_statement_page(ticker, '')
        income_rows = overview_rows
        balance_rows = {}
        cash_rows = overview_rows

        def make_frame(rows, mapping, amount=True):
            out = {}
            for label, aliases in mapping.items():
                found = None
                for alias in aliases:
                    key = alias.lower()
                    if key in rows:
                        found = rows[key][1]
                        break
                    partial = next((k for k in rows if key in k), None)
                    if partial is not None:
                        found = rows[partial][1]
                        break
                if found:
                    for year, value in found.items():
                        v = _stockanalysis_number(value, amount_in_millions=(amount and label not in ('Diluted EPS','Basic EPS')))
                        out.setdefault(label, {})[pd.Timestamp(year, 12, 31)] = v
            return pd.DataFrame(out).T.sort_index(axis=1) if out else pd.DataFrame()

        result['income'] = make_frame(income_rows, {
            'Total Revenue':['Revenue','Total Revenue'], 'Gross Profit':['Gross Profit'],
            'Operating Income':['Operating Income'], 'Net Income':['Net Income'],
            'Diluted EPS':['EPS','Diluted EPS','Earnings Per Share'], 'EBITDA':['EBITDA']
        })
        result['balance'] = make_frame(balance_rows, {
            'Total Assets':['Total Assets'], 'Stockholders Equity':['Total Equity','Total Stockholders Equity','Stockholders Equity'],
            'Total Debt':['Total Debt'], 'Cash And Cash Equivalents':['Cash & Cash Equivalents','Cash and Cash Equivalents'],
            'Current Assets':['Current Assets'], 'Current Liabilities':['Current Liabilities']
        })
        result['cashflow'] = make_frame(cash_rows, {
            'Operating Cash Flow':['Operating Cash Flow'], 'Capital Expenditure':['Capital Expenditures','Capital Expenditure'],
            'Free Cash Flow':['Free Cash Flow']
        })
        if result['income'].empty and result['balance'].empty and result['cashflow'].empty:
            result['error'] = 'StockAnalysis لم يُرجع جداول قابلة للقراءة.'
        else:
            result['field_sources'].update({k:'StockAnalysis' for k in ('income','balance','cashflow') if not result[k].empty})
    except Exception as exc:
        result['error'] = f"StockAnalysis: {str(exc)[:130]}"
    return result


def _mubasher_snapshot(symbol):
    """استخراج بيانات السهم الأساسية من صفحة معلومات مباشر؛ القوائم التفصيلية تظل من القوائم المنشورة."""
    ticker = symbol.replace('.CA', '').upper()
    result = _empty_financial_snapshot()
    result['source'] = 'Mubasher / معلومات مباشر'
    result['source_details'].append('Mubasher')
    try:
        url = f"https://www.mubasher.info/markets/EGX/stocks/{ticker}"
        response = requests.get(url, headers={"User-Agent":"Mozilla/5.0"}, timeout=12)
        response.raise_for_status()
        from bs4 import BeautifulSoup
        text = BeautifulSoup(response.text, 'html.parser').get_text(' ', strip=True)
        patterns = {
            'sharesOutstanding': r'عدد أسهم الشركة الحالي\s*([\d,]+)',
            'marketCap': r'القيمة السوقية\s*([\d,]+(?:\.\d+)?)',
            'bookValue': r'القيمة الدفترية\s*([\d,]+(?:\.\d+)?)',
            'trailingEps': r'ربحية السهم\s*([\d,]+(?:\.\d+)?)',
            'priceToBook': r'مضاعف القيمة الدفترية\s*([\d,]+(?:\.\d+)?)',
            'trailingPE': r'مضاعف الربحية\s*([\d,]+(?:\.\d+)?)',
        }
        for key, pattern in patterns.items():
            m = re.search(pattern, text)
            if m:
                result['info'][key] = float(m.group(1).replace(',', ''))
        if result['info']:
            result['field_sources'].update({k:'Mubasher' for k in result['info']})
        else:
            result['error'] = 'صفحة Mubasher لم تعرض حقولًا مالية قابلة للاستخراج.'
    except Exception as exc:
        result['error'] = f"Mubasher: {str(exc)[:130]}"
    return result


@st.cache_data(ttl=86400, show_spinner=False)
def get_financial_snapshot(symbol):
    """مصادر مالية متعددة فقط: Yahoo، StockAnalysis، Mubasher. لا تتدخل في محرك الأسعار الفني."""
    result = _empty_financial_snapshot()
    errors = []
    # المصدر الأول: Yahoo Finance
    try:
        ticker = yf.Ticker(symbol)
        for attr, key in (("financials", "income"), ("balance_sheet", "balance"), ("cashflow", "cashflow")):
            try:
                value = getattr(ticker, attr)
                if isinstance(value, pd.DataFrame) and not value.empty:
                    result[key] = value.copy()
                    result['field_sources'][key] = 'Yahoo Finance'
            except Exception:
                pass
        try:
            raw_info = ticker.get_info()
            if isinstance(raw_info, dict):
                allowed = ("shortName", "longName", "sector", "industry", "currency", "sharesOutstanding",
                    "impliedSharesOutstanding", "floatShares", "marketCap", "trailingEps", "forwardEps",
                    "trailingPE", "forwardPE", "priceToBook", "priceToSalesTrailing12Months", "enterpriseToEbitda",
                    "dividendYield", "trailingAnnualDividendRate", "quoteType", "totalRevenue", "netIncomeToCommon",
                    "bookValue", "totalCash", "totalDebt", "ebitda", "returnOnEquity", "returnOnAssets")
                result['info'] = {k:raw_info.get(k) for k in allowed if raw_info.get(k) is not None}
                result['field_sources'].update({k:'Yahoo Finance' for k in result['info']})
        except Exception as exc:
            errors.append(f"Yahoo info: {str(exc)[:70]}")
        try:
            div = ticker.dividends
            if isinstance(div, pd.Series): result['dividends'] = div.copy()
        except Exception: pass
    except Exception as exc:
        errors.append(f"Yahoo: {str(exc)[:90]}")

    # المصدر الثاني: StockAnalysis، يُستخدم لاستكمال القوائم الناقصة فقط.
    if any(result[k].empty for k in ('income','balance','cashflow')) or not result['info'].get('sharesOutstanding'):
        sa = _stockanalysis_snapshot(symbol)
        for key in ('income','balance','cashflow'):
            if result[key].empty and not sa[key].empty:
                result[key] = sa[key]
                result['field_sources'][key] = 'StockAnalysis'
        for key, value in sa['info'].items():
            if key not in result['info']: result['info'][key] = value
        if sa.get('error'): errors.append(sa['error'])
        if sa['field_sources']: result['source_details'].append('StockAnalysis')

    # المصدر الثالث: Mubasher للبيانات الأساسية/عدد الأسهم/EPS/BVPS عند غيابها.
    mu = _mubasher_snapshot(symbol)
    for key, value in mu['info'].items():
        if key not in result['info']:
            result['info'][key] = value
            result['field_sources'][key] = 'Mubasher'
    if mu.get('error'): errors.append(mu['error'])
    if mu['info']: result['source_details'].append('Mubasher')

    used = list(dict.fromkeys(result['field_sources'].values()))
    result['source'] = ' + '.join(used) if used else 'لا يوجد مصدر مالي متاح'
    result['error'] = ' | '.join(errors[:3])
    return result


def _financial_series(statement, aliases):
    if not isinstance(statement, pd.DataFrame) or statement.empty:
        return pd.Series(dtype=float)
    lookup = {str(idx).strip().lower(): idx for idx in statement.index}
    selected = None
    for alias in aliases:
        key = lookup.get(str(alias).strip().lower())
        if key is not None:
            selected = key
            break
    if selected is None:
        return pd.Series(dtype=float)
    row = statement.loc[selected]
    if isinstance(row, pd.DataFrame):
        row = row.iloc[0]
    try:
        cols = sorted(statement.columns, key=lambda x: pd.Timestamp(x), reverse=True)
        row = row.reindex(cols)
    except Exception:
        pass
    return pd.to_numeric(row, errors="coerce").dropna()


def _financial_latest(statement, aliases):
    values = _financial_series(statement, aliases)
    return float(values.iloc[0]) if not values.empty and np.isfinite(values.iloc[0]) else np.nan


def _financial_growth(statement, aliases):
    values = _financial_series(statement, aliases)
    if len(values) < 2:
        return np.nan
    old = float(values.iloc[1])
    new = float(values.iloc[0])
    if not np.isfinite(old) or old == 0 or not np.isfinite(new):
        return np.nan
    return (new / abs(old) - 1.0) * 100.0


def _financial_period(statement):
    if not isinstance(statement, pd.DataFrame) or statement.empty or len(statement.columns) == 0:
        return "غير متاح"
    try:
        return pd.Timestamp(max(statement.columns, key=lambda x: pd.Timestamp(x))).strftime("%Y-%m-%d")
    except Exception:
        return str(statement.columns[0])[:10]


def _score_up(value, low, high):
    try:
        value = float(value)
        if not np.isfinite(value):
            return np.nan
        return float(np.clip((value - low) / (high - low) * 100.0, 0, 100))
    except Exception:
        return np.nan


def _score_down(value, good, bad):
    try:
        value = float(value)
        if not np.isfinite(value):
            return np.nan
        return float(np.clip((bad - value) / (bad - good) * 100.0, 0, 100))
    except Exception:
        return np.nan



# =========================================================
# 🧭 التصنيف القطاعي الثابت لقائمة EGX AI PRO MAX (201 سهم)
# التصنيف مخصص للتحليل المالي فقط ولا يغير مصادر/منطق التداول الفني.
# =========================================================
SECTOR_GROUPS = {
    "البنوك": """COMI HDBK EGBE SAIB ADIB SAUD CIEB FAIT FAITA CANA EXPA""",
    "الخدمات المالية غير المصرفية": """EFIH BTFH CNFN OFH HRHO FWRY CCAP CICH AFDI PRMH ICLE EASB KWIN NAHO ACAMD ASPI DEIN MOIN ODIN BINV AMIA SEIG GRCA EBSC EOSB ATLC RKAZ OIH ELWA""",
    "العقارات والتطوير العمراني": """PHDC PRDC TMGH HELI EMFD OCDI ORHD MASR MAAL PHTV OBRI RREI NHPS GIHD AREH GPPL MMAT IDRE EGREF EHDR UNIT ZMID ELKA AMER DAPH RTVC ARAB CCRS FIRE""",
    "الرعاية الصحية والأدوية": """AMES BIOC CLHO MIPH MPCI AXPH CPCI NINH ADCI RMDA SPMD NIPH ISPH PHAR OCPH MEPA SIPC""",
    "الأغذية والمشروبات والزراعة": """IFAP ACGC INFI ZEOT SMFR UEFM WCDF EDFM MILS CEFM SCFM GSSC AJWA SUGR POUL DOMT ISMA MOSC COSG OLFI MPCO ELSH ELNA NEDA LUTS AIFI WKOL SNFC EPCO AALR EALR AFMC JUFO EFID EAST""",
    "الأسمدة والكيماويات والبتروكيماويات": """MFPC ABUK FERC EFIC KZPC MICH SKPC EGCH ICFC ICID""",
    "مواد البناء والمعادن والتعدين": """MBSC SVCE ARCC ASCM ISMQ EGAL ALUM IRON ATQA SCEM MCQE PRCL CERA LCSW MEGM COPR""",
    "الصناعات الهندسية والكهربائية والمعدات": """INEG ENGC GBCO SWDY ELEC MBEG EEII GDWA GMCI RUBX""",
    "المنسوجات والملابس والسلع المعمرة": """SPIN KABO APSW GTWL CFGH ORWE DSCW""",
    "الورق والتعبئة والتغليف والطباعة": """UNIP RAKT DTPP EPPK ADPC""",
    "النقل والشحن والخدمات البترولية": """ETRS CSAG ALCN MOIL NDRL TRTO""",
    "الطاقة والمرافق": """AMOC EGAS""",
    "الاتصالات والتكنولوجيا والإعلام": """ETEL SCTS EGSA MPRC AMPI RACC""",
    "السياحة والفنادق والترفيه": """EGTS MHOT SPHT SDTI ROTO MENA""",
    "التعليم والخدمات التعليمية": """CIRA MOED TALM CAED""",
    "المقاولات والتشييد والخدمات الهندسية": """GGCC NCCW UEGC ORAS FNAR""",
    "التجزئة والتوزيع والتجارة": """MTIE RAYA MFSC"""
}
SECTOR_BY_TICKER = {
    ticker: sector
    for sector, tickers in SECTOR_GROUPS.items()
    for ticker in tickers.split()
}

# هذه الرموز عليها مراجعة نشاط/قطاع قبل السماح بإصدار قيمة عادلة قطاعية.
SECTOR_REVIEW_TICKERS = {"EGSA", "COPR", "ICID", "ELWA", "GMCI", "OIH", "AIFI"}

# مضاعفات تقييم قطاعية افتراضية ومحافظة كبداية، قابلة للضبط بعد بناء قاعدة شركات مقارنة.
# لا تُستخدم مضاعفات EV/EBITDA للقطاعات التي لا يناسبها هذا المقياس.
SECTOR_PROFILES = {
    "البنوك": {
        "target_pe": 8.0, "target_ev_ebitda": None, "models": ("Residual Income", "P/E"),
        "rules": (("roe","up",0,25,25),("roa","up",0,2.5,15),("net_income_growth","up",-20,30,15),("pe","down",5,20,15),("pb","down",0.5,2.5,20),("dividend_yield","up",0,10,10))
    },
    "الخدمات المالية غير المصرفية": {
        "target_pe": 9.0, "target_ev_ebitda": 7.0, "models": ("Residual Income", "P/E"),
        "rules": (("roe","up",0,25,20),("roa","up",0,8,10),("net_margin","up",-5,25,10),("net_income_growth","up",-30,50,15),("debt_equity","down",0,2,15),("ocf_ni","up",-0.5,2,10),("pe","down",5,25,10),("pb","down",0.5,3,10))
    },
    "العقارات والتطوير العمراني": {
        "target_pe": 10.0, "target_ev_ebitda": None, "models": ("Residual Income", "P/E"),
        "rules": (("roe","up",0,20,15),("revenue_growth","up",-10,30,15),("net_margin","up",-5,25,15),("debt_equity","down",0,2,15),("current_ratio","up",0.5,2,10),("pe","down",5,25,15),("pb","down",0.5,3,15))
    },
    "الرعاية الصحية والأدوية": {
        "target_pe": 14.0, "target_ev_ebitda": 9.0, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("roe","up",0,25,15),("revenue_growth","up",-10,30,15),("net_margin","up",-5,25,15),("net_income_growth","up",-30,50,15),("debt_equity","down",0,2,10),("fcf_margin","up",-10,20,10),("ev_ebitda","down",4,18,10),("pe","down",5,30,10))
    },
    "الأغذية والمشروبات والزراعة": {
        "target_pe": 12.0, "target_ev_ebitda": 8.0, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("roe","up",0,25,15),("revenue_growth","up",-10,30,10),("net_margin","up",-5,20,15),("net_income_growth","up",-30,50,10),("debt_equity","down",0,2,15),("current_ratio","up",0.5,2,10),("ocf_ni","up",-0.5,2,10),("pe","down",5,25,10),("ev_ebitda","down",4,15,5))
    },
    "الأسمدة والكيماويات والبتروكيماويات": {
        "target_pe": 9.0, "target_ev_ebitda": 6.5, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("roe","up",0,25,10),("revenue_growth","up",-20,40,10),("operating_margin","up",-5,30,15),("net_income_growth","up",-30,50,10),("debt_equity","down",0,2,15),("fcf_margin","up",-10,25,15),("ev_ebitda","down",3,15,15),("pe","down",4,25,10))
    },
    "مواد البناء والمعادن والتعدين": {
        "target_pe": 9.0, "target_ev_ebitda": 6.5, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("revenue_growth","up",-20,40,10),("operating_margin","up",-5,30,15),("roe","up",0,25,10),("debt_equity","down",0,2,15),("current_ratio","up",0.5,2,10),("fcf_margin","up",-10,25,15),("ev_ebitda","down",3,15,15),("pe","down",4,25,10))
    },
    "الصناعات الهندسية والكهربائية والمعدات": {
        "target_pe": 10.0, "target_ev_ebitda": 7.0, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("revenue_growth","up",-10,35,15),("operating_margin","up",-5,25,15),("roe","up",0,25,10),("debt_equity","down",0,2,15),("current_ratio","up",0.5,2,10),("ocf_ni","up",-0.5,2,15),("ev_ebitda","down",3,16,10),("pe","down",4,25,10))
    },
    "المنسوجات والملابس والسلع المعمرة": {
        "target_pe": 9.0, "target_ev_ebitda": 6.0, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("revenue_growth","up",-15,30,10),("gross_margin","up",5,40,15),("net_margin","up",-5,20,15),("roe","up",0,25,10),("debt_equity","down",0,2,15),("current_ratio","up",0.5,2,10),("fcf_margin","up",-10,20,10),("pe","down",4,25,10),("ev_ebitda","down",3,15,5))
    },
    "الورق والتعبئة والتغليف والطباعة": {
        "target_pe": 9.0, "target_ev_ebitda": 6.0, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("revenue_growth","up",-15,30,10),("gross_margin","up",5,40,15),("net_margin","up",-5,20,15),("roe","up",0,25,10),("debt_equity","down",0,2,15),("current_ratio","up",0.5,2,10),("fcf_margin","up",-10,20,10),("pe","down",4,25,10),("ev_ebitda","down",3,15,5))
    },
    "النقل والشحن والخدمات البترولية": {
        "target_pe": 9.0, "target_ev_ebitda": 6.5, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("roe","up",0,20,10),("operating_margin","up",-5,25,15),("revenue_growth","up",-15,30,10),("debt_equity","down",0,2,15),("current_ratio","up",0.5,2,10),("fcf_margin","up",-10,25,15),("ev_ebitda","down",3,15,15),("pe","down",4,25,10))
    },
    "الطاقة والمرافق": {
        "target_pe": 8.0, "target_ev_ebitda": 5.5, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("roe","up",0,20,10),("operating_margin","up",-5,30,15),("fcf_margin","up",-10,30,20),("debt_equity","down",0,2,15),("revenue_growth","up",-20,30,10),("ev_ebitda","down",3,12,15),("pe","down",4,22,10),("current_ratio","up",0.5,2,5))
    },
    "الاتصالات والتكنولوجيا والإعلام": {
        "target_pe": 11.0, "target_ev_ebitda": 6.5, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("roe","up",0,25,15),("operating_margin","up",0,35,15),("revenue_growth","up",-10,30,10),("debt_equity","down",0,2,10),("fcf_margin","up",-10,30,20),("ev_ebitda","down",3,15,15),("pe","down",5,30,5),("dividend_yield","up",0,10,5))
    },
    "السياحة والفنادق والترفيه": {
        "target_pe": 10.0, "target_ev_ebitda": 7.0, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("revenue_growth","up",-20,40,15),("operating_margin","up",-10,30,15),("roe","up",0,20,10),("debt_equity","down",0,2,15),("current_ratio","up",0.5,2,10),("fcf_margin","up",-15,25,15),("ev_ebitda","down",3,16,10),("pe","down",4,25,10))
    },
    "التعليم والخدمات التعليمية": {
        "target_pe": 12.0, "target_ev_ebitda": 8.0, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("revenue_growth","up",-10,35,15),("operating_margin","up",0,35,15),("roe","up",0,25,15),("debt_equity","down",0,2,10),("current_ratio","up",0.5,2,10),("fcf_margin","up",-10,25,15),("ev_ebitda","down",4,18,10),("pe","down",5,30,10))
    },
    "المقاولات والتشييد والخدمات الهندسية": {
        "target_pe": 8.0, "target_ev_ebitda": 6.0, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("revenue_growth","up",-20,40,15),("operating_margin","up",-5,25,15),("roe","up",0,20,10),("debt_equity","down",0,2,15),("current_ratio","up",0.5,2,10),("ocf_ni","up",-0.5,2,15),("ev_ebitda","down",3,15,10),("pe","down",4,22,10))
    },
    "التجزئة والتوزيع والتجارة": {
        "target_pe": 10.0, "target_ev_ebitda": 7.5, "models": ("DCF", "EV/EBITDA", "P/E"),
        "rules": (("revenue_growth","up",-10,35,15),("net_margin","up",-5,20,10),("roe","up",0,25,15),("debt_equity","down",0,2,10),("current_ratio","up",0.5,2,10),("ocf_ni","up",-0.5,2,15),("pe","down",4,25,15),("ev_ebitda","down",3,16,10))
    }
}

def get_sector_classification(symbol):
    ticker = str(symbol).replace(".CA", "").upper()
    sector = SECTOR_BY_TICKER.get(ticker, "غير مصنف")
    review = ticker in SECTOR_REVIEW_TICKERS or sector == "غير مصنف"
    profile = SECTOR_PROFILES.get(sector, {})
    return {
        "ticker": ticker,
        "sector": sector,
        "status": "معلّق للمراجعة" if review else "معتمد مبدئيًا",
        "profile": profile,
        "review": review
    }

def calculate_financial_metrics(symbol, snapshot, latest_close=np.nan, price_date="", cost_equity_pct=18.0,
                                base_growth_pct=5.0, terminal_growth_pct=3.0, target_pe=10.0):
    """تحليل مالي محافظ؛ لا يستبدل البيانات المفقودة بأرقام تقديرية."""
    income = snapshot.get("income", pd.DataFrame())
    balance = snapshot.get("balance", pd.DataFrame())
    cashflow = snapshot.get("cashflow", pd.DataFrame())
    info = snapshot.get("info", {}) or {}
    sector_data = get_sector_classification(symbol)
    sector_name = sector_data["sector"]
    sector_profile = sector_data["profile"]

    revenue = _financial_latest(income, ["Total Revenue", "Operating Revenue", "Revenue", "TotalRevenue"])
    if not np.isfinite(revenue):
        try: revenue = float(info.get("totalRevenue", np.nan))
        except Exception: pass
    gross_profit = _financial_latest(income, ["Gross Profit", "GrossProfit"])
    operating_income = _financial_latest(income, ["Operating Income", "Operating Income Loss", "OperatingIncome"])
    net_income = _financial_latest(income, ["Net Income", "Net Income Common Stockholders", "Net Income Continuous Operations", "NetIncome", "Net Income From Continuing Operations"])
    if not np.isfinite(net_income):
        try: net_income = float(info.get("netIncomeToCommon", np.nan))
        except Exception: pass
    eps = _financial_latest(income, ["Diluted EPS", "Basic EPS", "DilutedEPS", "BasicEPS"])
    eps_values = _financial_series(income, ["Diluted EPS", "Basic EPS", "DilutedEPS", "BasicEPS"])
    eps_normalized = float(eps_values.head(3).median()) if len(eps_values) >= 2 else eps
    if not np.isfinite(eps):
        try: eps = float(info.get("trailingEps", np.nan))
        except Exception: eps = np.nan
    if not np.isfinite(eps_normalized): eps_normalized = eps

    total_assets = _financial_latest(balance, ["Total Assets"])
    equity = _financial_latest(balance, ["Stockholders Equity", "Total Stockholder Equity", "Total Equity Gross Minority Interest", "Common Stock Equity", "StockholdersEquity", "TotalEquityGrossMinorityInterest"])
    current_assets = _financial_latest(balance, ["Current Assets", "Total Current Assets"])
    current_liabilities = _financial_latest(balance, ["Current Liabilities", "Total Current Liabilities"])
    total_debt = _financial_latest(balance, ["Total Debt"])
    if not np.isfinite(total_debt):
        short_debt = _financial_latest(balance, ["Current Debt", "Short Long Term Debt", "Current Debt And Capital Lease Obligation"])
        long_debt = _financial_latest(balance, ["Long Term Debt", "Long Term Debt And Capital Lease Obligation"])
        if np.isfinite(short_debt) or np.isfinite(long_debt):
            total_debt = np.nan_to_num(short_debt) + np.nan_to_num(long_debt)
    cash = _financial_latest(balance, ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments", "Cash And Short Term Investments"])

    operating_cashflow = _financial_latest(cashflow, ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities", "Total Cash From Operating Activities", "OperatingCashFlow"])
    capex = _financial_latest(cashflow, ["Capital Expenditure", "Capital Expenditures", "CapitalExpenditure"])
    free_cashflow = np.nan
    if np.isfinite(operating_cashflow) and np.isfinite(capex):
        free_cashflow = operating_cashflow + capex if capex < 0 else operating_cashflow - capex
    elif np.isfinite(_financial_latest(cashflow, ["Free Cash Flow"])):
        free_cashflow = _financial_latest(cashflow, ["Free Cash Flow"])

    price = float(latest_close) if pd.notna(latest_close) else np.nan
    shares = info.get("sharesOutstanding", info.get("impliedSharesOutstanding", info.get("floatShares", np.nan)))
    try: shares = float(shares)
    except Exception: shares = np.nan
    # Yahoo قد لا يعيد sharesOutstanding لبعض أسهم EGX؛ يمكن اشتقاقه من القيمة السوقية والسعر إذا توافرا.
    if (not np.isfinite(shares) or shares <= 0) and np.isfinite(price) and price > 0:
        try:
            market_cap_for_shares = float(info.get("marketCap", np.nan))
            if np.isfinite(market_cap_for_shares) and market_cap_for_shares > 0:
                shares = market_cap_for_shares / price
        except Exception:
            pass
    # Mubasher يورد Book Value للسهم؛ نستنتج إجمالي حقوق الملكية فقط عند توافر عدد الأسهم من مصدر.
    if (not np.isfinite(equity) or equity <= 0) and np.isfinite(shares) and shares > 0:
        try:
            source_bvps = float(info.get("bookValue", np.nan))
            if np.isfinite(source_bvps) and source_bvps > 0:
                equity = source_bvps * shares
        except Exception:
            pass
    bvps = equity / shares if np.isfinite(equity) and np.isfinite(shares) and shares > 0 else np.nan
    roe = net_income / equity * 100.0 if np.isfinite(net_income) and np.isfinite(equity) and equity > 0 else np.nan
    roa = net_income / total_assets * 100.0 if np.isfinite(net_income) and np.isfinite(total_assets) and total_assets > 0 else np.nan
    gross_margin = gross_profit / revenue * 100.0 if np.isfinite(gross_profit) and np.isfinite(revenue) and revenue > 0 else np.nan
    operating_margin = operating_income / revenue * 100.0 if np.isfinite(operating_income) and np.isfinite(revenue) and revenue > 0 else np.nan
    net_margin = net_income / revenue * 100.0 if np.isfinite(net_income) and np.isfinite(revenue) and revenue > 0 else np.nan
    current_ratio = current_assets / current_liabilities if np.isfinite(current_assets) and np.isfinite(current_liabilities) and current_liabilities > 0 else np.nan
    debt_equity = total_debt / equity if np.isfinite(total_debt) and np.isfinite(equity) and equity > 0 else np.nan
    ocf_ni = operating_cashflow / net_income if np.isfinite(operating_cashflow) and np.isfinite(net_income) and net_income != 0 else np.nan
    fcf_margin = free_cashflow / revenue * 100.0 if np.isfinite(free_cashflow) and np.isfinite(revenue) and revenue > 0 else np.nan
    revenue_growth = _financial_growth(income, ["Total Revenue", "Operating Revenue", "Revenue"])
    net_income_growth = _financial_growth(income, ["Net Income", "Net Income Common Stockholders", "Net Income Continuous Operations"])
    pe = price / eps if np.isfinite(price) and np.isfinite(eps) and eps > 0 else np.nan
    pb = price / bvps if np.isfinite(price) and np.isfinite(bvps) and bvps > 0 else np.nan
    ps = price / (revenue / shares) if np.isfinite(price) and np.isfinite(revenue) and np.isfinite(shares) and shares > 0 and revenue > 0 else np.nan
    ebitda = _financial_latest(income, ["EBITDA", "Normalized EBITDA"])
    market_cap = price * shares if np.isfinite(price) and np.isfinite(shares) and shares > 0 else np.nan
    ev_ebitda = (market_cap + np.nan_to_num(total_debt) - np.nan_to_num(cash)) / ebitda if np.isfinite(market_cap) and np.isfinite(ebitda) and ebitda > 0 else np.nan

    dividend_yield = np.nan
    try:
        raw_yield = float(info.get("dividendYield", np.nan))
        if np.isfinite(raw_yield): dividend_yield = raw_yield * 100.0 if abs(raw_yield) <= 1 else raw_yield
    except Exception: pass
    if not np.isfinite(dividend_yield) and np.isfinite(price) and price > 0:
        divs = snapshot.get("dividends", pd.Series(dtype=float))
        try:
            if isinstance(divs, pd.Series) and not divs.empty:
                cutoff = pd.Timestamp.now(tz=None) - pd.Timedelta(days=365)
                annual_div = pd.to_numeric(divs[divs.index >= cutoff], errors="coerce").sum()
                dividend_yield = float(annual_div / price * 100.0)
        except Exception: pass

    # درجة مالية قطاعية: تختلف المؤشرات وأوزانها حسب طبيعة النشاط.
    score_metric_values = {
        "roe": roe, "roa": roa, "net_margin": net_margin,
        "revenue_growth": revenue_growth, "net_income_growth": net_income_growth,
        "current_ratio": current_ratio, "debt_equity": debt_equity,
        "ocf_ni": ocf_ni, "fcf_margin": fcf_margin, "pe": pe, "pb": pb,
        "operating_margin": operating_margin, "gross_margin": gross_margin,
        "ev_ebitda": ev_ebitda, "dividend_yield": dividend_yield
    }
    sector_rules = sector_profile.get("rules", ())
    valid_parts = []
    for metric_key, direction, low, high, weight in sector_rules:
        metric_value = score_metric_values.get(metric_key, np.nan)
        metric_score = _score_up(metric_value, low, high) if direction == "up" else _score_down(metric_value, low, high)
        if np.isfinite(metric_score):
            valid_parts.append((metric_score, weight))
    coverage = sum(weight for _, weight in valid_parts)
    financial_score = sum(value * weight for value, weight in valid_parts) / coverage if coverage >= 35 and not sector_data["review"] else np.nan

    # تقييم DCF مبسط للتدفق الحر، وResidual Income للمنشآت المالية وغيرها عند توافر المدخلات.
    ke = float(cost_equity_pct) / 100.0
    growth = float(base_growth_pct) / 100.0
    terminal_growth = float(terminal_growth_pct) / 100.0
    if terminal_growth >= ke:
        terminal_growth = max(0.0, ke - 0.01)
    dcf_value = np.nan
    if np.isfinite(free_cashflow) and free_cashflow > 0 and np.isfinite(shares) and shares > 0 and ke > terminal_growth:
        fcf_ps = free_cashflow / shares
        pv = 0.0
        for year in range(1, 6):
            forecast = fcf_ps * ((1.0 + growth) ** year)
            pv += forecast / ((1.0 + ke) ** year)
        terminal_fcf = fcf_ps * ((1.0 + growth) ** 5) * (1.0 + terminal_growth)
        terminal_value = terminal_fcf / (ke - terminal_growth)
        dcf_value = pv + terminal_value / ((1.0 + ke) ** 5)
        if not np.isfinite(dcf_value) or dcf_value <= 0: dcf_value = np.nan

    residual_value = np.nan
    if np.isfinite(bvps) and bvps > 0 and np.isfinite(roe) and ke > growth:
        roe_decimal = roe / 100.0
        residual_value = bvps + ((roe_decimal - ke) * bvps) / (ke - growth)
        if not np.isfinite(residual_value) or residual_value <= 0: residual_value = np.nan

    # نماذج التقييم تختلف حسب القطاع. مضاعفات القطاعات افتراضات معلنة وليست حقائق سوقية.
    try:
        global_pe_reference = float(target_pe)
        if not np.isfinite(global_pe_reference) or global_pe_reference <= 0:
            global_pe_reference = 10.0
    except Exception:
        global_pe_reference = 10.0
    pe_adjustment = global_pe_reference / 10.0
    sector_target_pe = float(sector_profile.get("target_pe", 10.0)) * pe_adjustment
    if np.isfinite(eps_normalized) and eps_normalized > 0:
        earnings_value = eps_normalized * sector_target_pe
    else:
        earnings_value = np.nan
    graham_value = np.sqrt(22.5 * eps_normalized * bvps) if np.isfinite(eps_normalized) and eps_normalized > 0 and np.isfinite(bvps) and bvps > 0 else np.nan

    sector_target_ev = sector_profile.get("target_ev_ebitda")
    ev_ebitda_value = np.nan
    if sector_target_ev is not None and np.isfinite(ebitda) and ebitda > 0 and np.isfinite(shares) and shares > 0:
        debt_for_ev = total_debt if np.isfinite(total_debt) else 0.0
        cash_for_ev = cash if np.isfinite(cash) else 0.0
        candidate_ev_value = (ebitda * float(sector_target_ev) - debt_for_ev + cash_for_ev) / shares
        if np.isfinite(candidate_ev_value) and candidate_ev_value > 0:
            ev_ebitda_value = float(candidate_ev_value)

    valuation_method = "غير متاح"
    valuation_reason = ""
    fair_value = np.nan
    allowed_models = sector_profile.get("models", ())
    model_values = {}
    if not sector_data["review"]:
        model_lookup = {
            "DCF": dcf_value,
            "EV/EBITDA": ev_ebitda_value,
            "Residual Income": residual_value,
            "P/E": earnings_value
        }
        model_values = {name: model_lookup.get(name, np.nan) for name in allowed_models}
    valid_models = {name: float(value) for name, value in model_values.items() if np.isfinite(value) and value > 0}
    if valid_models:
        # الوسيط بين النماذج المسموح بها للقطاع فقط، ولا يتم خلط قطاعات مختلفة.
        fair_value = float(np.median(list(valid_models.values())))
        valuation_method = "وسيط نماذج القطاع: " + " + ".join(valid_models.keys())

    if sector_data["review"]:
        valuation_reason = "تصنيف القطاع معلّق للمراجعة؛ تم إيقاف القيمة العادلة القطاعية لحين تأكيد النشاط."
    elif not np.isfinite(fair_value):
        missing = []
        for model_name in allowed_models:
            if model_name == "DCF" and not np.isfinite(dcf_value):
                missing.append("تدفقات نقدية حرة موجبة وعدد أسهم صالح لنموذج DCF")
            elif model_name == "EV/EBITDA" and not np.isfinite(ev_ebitda_value):
                missing.append("EBITDA موجب والديون/النقد وعدد الأسهم لنموذج EV/EBITDA")
            elif model_name == "Residual Income" and not np.isfinite(residual_value):
                missing.append("حقوق ملكية وربحية وROE صالح لنموذج Residual Income")
            elif model_name == "P/E" and not np.isfinite(earnings_value):
                missing.append("ربحية سهم طبيعية موجبة لنموذج P/E")
        valuation_reason = "المدخلات غير مكتملة للنماذج القطاعية: " + "؛ ".join(dict.fromkeys(missing)) if missing else "النماذج القطاعية المتاحة لا تنتج قيمة موجبة."

    upside = (fair_value / price - 1.0) * 100.0 if np.isfinite(fair_value) and np.isfinite(price) and price > 0 else np.nan
    valuation_confidence = min(100.0, coverage * 0.55 + min(len(valid_models), 3) * 15 + (10 if not sector_data["review"] else 0))
    if coverage < 25:
        status = "⚪ بيانات مالية غير كافية"
    elif coverage < 50:
        status = "🟡 تغطية مالية محدودة"
    else:
        status = "✅ تحليل مالي متاح"

    period = max((_financial_period(x) for x in (income, balance, cashflow) if isinstance(x, pd.DataFrame) and not x.empty), default="غير متاح")
    return {
        "السهم": symbol.replace(".CA", ""), "الحالة المالية": status,
        "التقييم المالي": round(financial_score, 2) if np.isfinite(financial_score) else np.nan,
        "تغطية البيانات %": round(coverage, 1), "الإيرادات": revenue,
        "نمو الإيرادات %": revenue_growth, "مجمل الربح": gross_profit,
        "الربح التشغيلي": operating_income, "صافي الربح": net_income,
        "نمو صافي الربح %": net_income_growth, "EPS": eps, "EPS طبيعي 3 سنوات": eps_normalized,
        "ROE %": roe, "ROA %": roa, "هامش مجمل الربح %": gross_margin,
        "هامش التشغيل %": operating_margin, "هامش صافي الربح %": net_margin,
        "إجمالي الأصول": total_assets, "حقوق الملكية": equity, "إجمالي الديون": total_debt,
        "الدين/حقوق الملكية": debt_equity, "Current Ratio": current_ratio,
        "التدفق النقدي التشغيلي": operating_cashflow, "CapEx": capex,
        "Free Cash Flow": free_cashflow, "FCF Margin %": fcf_margin,
        "P/E": pe, "P/B": pb, "P/S": ps, "EV/EBITDA": ev_ebitda,
        "Dividend Yield %": dividend_yield, "قيمة DCF": dcf_value, "قيمة Residual Income": residual_value,
        "قيمة Graham": graham_value, "قيمة مضاعف الأرباح": earnings_value,
        "قيمة EV/EBITDA": ev_ebitda_value,
        "مضاعف EV/EBITDA القطاعي": sector_target_ev if sector_target_ev is not None else np.nan,
        "مضاعف P/E القطاعي": sector_target_pe,
        "نماذج القطاع": " + ".join(allowed_models) if allowed_models else "غير متاح",
        "عدد النماذج المتاحة": len(valid_models), "القيمة العادلة": fair_value,
        "شراء -10%": fair_value * 0.90 if np.isfinite(fair_value) else np.nan,
        "شراء -20%": fair_value * 0.80 if np.isfinite(fair_value) else np.nan,
        "شراء -30%": fair_value * 0.70 if np.isfinite(fair_value) else np.nan,
        "Upside %": upside, "منهج التقييم": valuation_method,
        "سبب عدم توافر القيمة العادلة": valuation_reason,
        "ثقة التقييم %": round(valuation_confidence, 1),
        "القطاع": sector_name, "حالة التصنيف": sector_data["status"],
        "مصدر التصنيف": "تصنيف EGX AI PRO MAX اليدوي" if not sector_data["review"] else "معلّق للمراجعة",
        "قطاع Yahoo": info.get("sector", "غير متاح"), "الصناعة": info.get("industry", "غير متاح"),
        "تاريخ آخر قائمة": period, "تاريخ السعر": price_date or "غير متاح",
        "المصدر": snapshot.get("source", "غير متاح"),
        "مصادر الحقول": "؛ ".join(f"{k}: {v}" for k, v in snapshot.get("field_sources", {}).items()),
        "رابط StockAnalysis": f"https://stockanalysis.com/quote/egx/{symbol.replace('.CA','').upper()}/financials/",
        "رابط Mubasher": f"https://www.mubasher.info/markets/EGX/stocks/{symbol.replace('.CA','').upper()}",
        "رابط EGX الرسمي": "https://www.egx.com.eg/",
        "ملاحظة المصدر": snapshot.get("error", "")
    }


def scan_financial_universe(symbols, daily_data, raw_price_data, workers, cost_equity_pct, base_growth_pct, terminal_growth_pct, target_pe):
    """فحص مالي منفصل، مع Close غير معدل واستبعاد شمعة اليوم قبل 15:00 بتوقيت القاهرة."""
    rows = []
    def worker(symbol):
        try:
            d = extract_symbol_data(raw_price_data, symbol)
            price_source = "Yahoo Finance Daily Close غير معدل"
            if d.empty or "Close" not in d.columns:
                d = extract_symbol_data(daily_data, symbol)
                price_source = "Daily Close بديل من محرك الفحص"
            close = np.nan
            close_date = "غير متاح"
            if not d.empty and "Close" in d.columns:
                vals = pd.to_numeric(d["Close"], errors="coerce").dropna()
                if not vals.empty:
                    cairo_now = pd.Timestamp.now(tz="Africa/Cairo")
                    latest_day = pd.Timestamp(vals.index[-1]).date()
                    if latest_day == cairo_now.date() and (cairo_now.hour, cairo_now.minute) < (15, 0) and len(vals) > 1:
                        vals = vals.iloc[:-1]
                    if not vals.empty:
                        close = float(vals.iloc[-1])
                        close_date = pd.Timestamp(vals.index[-1]).strftime("%Y-%m-%d")
            snap = get_financial_snapshot(symbol)
            row = calculate_financial_metrics(symbol, snap, close, close_date, cost_equity_pct, base_growth_pct, terminal_growth_pct, target_pe)
            row["مصدر السعر"] = price_source
            return row
        except Exception as exc:
            return {"السهم": symbol.replace(".CA", ""), "الحالة المالية": "❌ تعذر التحليل", "ملاحظة المصدر": str(exc)[:160]}
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(worker, symbol): symbol for symbol in symbols}
        progress = st.progress(0)
        status = st.empty()
        for i, future in enumerate(as_completed(futures), start=1):
            try:
                rows.append(future.result())
            except Exception as exc:
                symbol = futures[future]
                rows.append({"السهم": symbol.replace(".CA", ""), "الحالة المالية": "❌ تعذر التحليل", "ملاحظة المصدر": str(exc)[:160]})
            progress.progress(i / max(len(symbols), 1))
            status.info(f"🏦 جاري التحليل المالي: {i} من {len(symbols)}")
        status.success("✅ انتهى فحص القوائم المالية المتاحة")
    out = pd.DataFrame(rows)
    if not out.empty and "التقييم المالي" in out.columns:
        if "القطاع" in out.columns and "حالة التصنيف" in out.columns:
            confirmed = out["حالة التصنيف"].eq("معتمد مبدئيًا")
            out["ترتيب داخل القطاع"] = np.nan
            out.loc[confirmed, "ترتيب داخل القطاع"] = (
                out.loc[confirmed].groupby("القطاع")["التقييم المالي"]
                .rank(method="min", ascending=False)
            )
        out = out.sort_values("التقييم المالي", ascending=False, na_position="last").reset_index(drop=True)
        out.insert(0, "الترتيب المالي", np.arange(1, len(out) + 1))
    return out


# =========================================================
# 🧠 التحليل الرئيسي
# =========================================================

def analyze(
    df_d,
    df_w,
    df_m,
    capital,
    risk_percent
):

    df_d = add_indicators(
        df_d
    )

    df_w = add_indicators(
        df_w
    )

    df_m = add_indicators(
        df_m
    )

    # =====================================================
    # التأكد من البيانات
    # =====================================================

    if len(df_d) < MIN_DAILY_ROWS:
        raise ValueError(
            "بيانات يومية غير كافية"
        )

    if len(df_w) < MIN_WEEKLY_ROWS:
        raise ValueError(
            "بيانات أسبوعية غير كافية"
        )

    if len(df_m) < MIN_MONTHLY_ROWS:
        raise ValueError(
            "بيانات شهرية غير كافية"
        )

    # =====================================================
    # Data Quality
    # =====================================================

    quality_d = calculate_data_quality(
        df_d
    )

    quality_w = calculate_data_quality(
        df_w
    )

    quality_m = calculate_data_quality(
        df_m
    )

    data_quality = (
        quality_d["quality"] * 0.50 +
        quality_w["quality"] * 0.30 +
        quality_m["quality"] * 0.20
    )

    # =====================================================
    # تنظيف المؤشرات
    # =====================================================

    required_daily = [
        "ema20",
        "ema50",
        "rsi",
        "macd",
        "macd_signal",
        "macd_hist",
        "vol_ma",
        "volume_ratio",
        "obv",
        "obv_ma",
        "obv_slope",
        "mfi",
        "stoch_rsi",
        "stoch_rsi_k",
        "stoch_rsi_d",
        "stoch_rsi_k_slope",
        "vwap",
        "support",
        "resistance",
        "previous_support",
        "previous_resistance",
        "atr",
        "adx",
        "ema20_slope",
        "ema50_slope",
        "body_pct"
    ]

    required_tf = [
        "ema20",
        "ema50",
        "macd",
        "macd_signal",
        "rsi",
        "ema20_slope"
    ]

    # EMA200 لا يدخل في required_tf
    # لأننا نريد معرفة هل هو مكتمل أم لا
    df_d = df_d.dropna(
        subset=required_daily
    )

    df_w = df_w.dropna(
        subset=required_tf
    )

    df_m = df_m.dropna(
        subset=required_tf
    )

    if (
        df_d.empty or
        df_w.empty or
        df_m.empty
    ):

        raise ValueError(
            "المؤشرات غير متاحة"
        )

    # =====================================================
    # آخر قراءة
    # =====================================================

    last_d = df_d.iloc[-1]
    last_w = df_w.iloc[-1]
    last_m = df_m.iloc[-1]

    market_price = float(
        last_d["Close"]
    )

    if market_price <= 0:
        raise ValueError(
            "سعر غير صحيح"
        )

    # =====================================================
    # Liquidity + Relative Strength
    # =====================================================
    liquidity_ratio = float(last_d.get("liquidity_ratio", np.nan))
    if not np.isfinite(liquidity_ratio):
        liquidity_ratio = 0.0
    stock_return_20 = float(last_d.get("return_20d", np.nan))
    market_return_20 = float(last_d.get("market_return_20", np.nan))
    if not np.isfinite(stock_return_20):
        stock_return_20 = 0.0
    if not np.isfinite(market_return_20):
        market_return_20 = 0.0
    relative_strength = stock_return_20 - market_return_20
    liquidity_score = 5 if liquidity_ratio >= 2 else 4 if liquidity_ratio >= 1.5 else 3 if liquidity_ratio >= 1.0 else 1 if liquidity_ratio >= 0.7 else 0
    rs_score = 5 if relative_strength >= 0.10 else 4 if relative_strength >= 0.05 else 3 if relative_strength >= 0 else 1 if relative_strength >= -0.05 else 0

    # =====================================================
    # EMA200 Quality
    # =====================================================

    daily_ema200_complete = (
        len(df_d) >= EMA200_REQUIRED_ROWS
    )

    weekly_ema200_complete = (
        len(df_w) >= EMA200_REQUIRED_ROWS
    )

    monthly_ema200_complete = (
        len(df_m) >= EMA200_REQUIRED_ROWS
    )

    ema200_status = (
        "✅ مكتمل"
        if (
            daily_ema200_complete and
            weekly_ema200_complete and
            monthly_ema200_complete
        )
        else "⚠️ غير مكتمل"
    )

    # =====================================================
    # Trend Alignment
    # =====================================================

    alignment = trend_alignment_score(
        df_d,
        df_w,
        df_m
    )

    # نسبة الشراء للعرض فقط — لا تؤثر على Score أو Ranking أو Entry/Risk.
    buy_percentage = calculate_buy_percentage(
        last_d,
        last_w,
        last_m,
        alignment,
        relative_strength
    )

    # =====================================================
    # Market Regime
    # =====================================================

    regime = market_regime(
        last_d
    )

    # =====================================================
    # Entry Engine
    # =====================================================

    entry_info = determine_entry(
        df_d,
        alignment
    )

    entry = float(
        entry_info["price"]
    )

    entry_type = entry_info["type"]
    entry_reason = entry_info["reason"]

    # =====================================================
    # Risk / Target Engine
    # =====================================================

    risk = calculate_risk_engine(
        df_d,
        entry,
        capital,
        risk_percent,
        df_w,
        df_m
    )

    stop = risk["stop"]

    tp1 = risk["tp1"]
    tp2 = risk["tp2"]
    tp3 = risk["tp3"]
    tp4 = risk["tp4"]

    # =====================================================
    # Score جديد من 100
    #
    # 25 Trend
    # 15 Momentum
    # 15 Volume / Money Flow
    # 10 Trend Strength
    # 10 Price Structure
    # 10 Entry Quality
    # 10 Target Quality
    # 5 Risk
    #
    # TOTAL = 100
    # =====================================================

    score = 0.0

    # =====================================================
    # 1. Trend Quality = 25
    #
    # لا نكرر EMA20/50/200 بشكل زائد
    # =====================================================

    trend_component = (
        alignment * 0.25
    )

    score += trend_component

    # =====================================================
    # 2. Momentum = 15
    # =====================================================

    rsi = float(
        last_d["rsi"]
    )

    momentum_score = 0

    if 50 <= rsi <= 65:
        momentum_score += 7

    elif 45 <= rsi < 50:
        momentum_score += 5

    elif 65 < rsi <= 70:
        momentum_score += 5

    elif 35 <= rsi < 45:
        momentum_score += 2

    if (
        last_d["macd"] >
        last_d["macd_signal"]
    ):
        momentum_score += 5

    elif last_d["macd_hist"] > 0:
        momentum_score += 3

    stoch_k = float(
        last_d["stoch_rsi_k"]
    )

    stoch_d = float(
        last_d["stoch_rsi_d"]
    )

    if stoch_k > stoch_d:
        momentum_score += 3

    score += min(
        15,
        momentum_score
    )

    # =====================================================
    # 3. Volume / Money Flow = 10
    # =====================================================

    volume_ratio = float(
        last_d["volume_ratio"]
    )

    money_score = 0

    if volume_ratio >= 2:
        money_score += 5

    elif volume_ratio >= 1.5:
        money_score += 4

    elif volume_ratio >= 1.1:
        money_score += 3

    elif volume_ratio >= 0.8:
        money_score += 1

    mfi = float(
        last_d["mfi"]
    )

    if 50 <= mfi <= 75:
        money_score += 4

    elif 40 <= mfi < 50:
        money_score += 2

    elif 75 < mfi <= 85:
        money_score += 2

    obv = float(
        last_d["obv"]
    )

    obv_ma = float(
        last_d["obv_ma"]
    )

    obv_slope = float(
        last_d["obv_slope"]
    )

    if (
        obv > obv_ma and
        obv_slope > 0
    ):
        money_score += 6

    elif (
        obv > obv_ma or
        obv_slope > 0
    ):
        money_score += 4

    elif obv_slope > 0:
        money_score += 2

    score += min(
        10,
        money_score
    )

    # =====================================================
    # 4. Trend Strength = 5
    # =====================================================

    adx_val = float(
        last_d["adx"]
    )

    strength_score = 0

    if adx_val >= 30:
        strength_score = 5
    elif adx_val >= 25:
        strength_score = 4
    elif adx_val >= 20:
        strength_score = 3
    elif adx_val >= 15:
        strength_score = 1.5

    # V9: cap ADX contribution at the declared 5 points.
    score += min(5, strength_score)

    # =====================================================
    # 5. Price Structure = 10
    # =====================================================

    structure_score = 0

    if (
        last_d["ema20_slope"] > 0 and
        last_d["ema50_slope"] > 0
    ):
        structure_score += 4

    elif last_d["ema20_slope"] > 0:
        structure_score += 2

    if (
        last_d["Close"] >
        last_d["vwap"]
    ):
        structure_score += 3

    if (
        last_d["Close"] >
        last_d["ema50"]
    ):
        structure_score += 3

    score += min(
        10,
        structure_score
    )

    # =====================================================
    # 6. Entry Quality = 10
    # =====================================================

    entry_score = 0

    if entry_type == "دخول عند Pullback":
        entry_score = 10

    elif entry_type == "دخول اختراق":
        entry_score = 9

    elif entry_type == "دخول فوري":
        entry_score = 7

    else:
        entry_score = 2

    score += entry_score

    # =====================================================
    # 7. Target Quality = 10
    # =====================================================

    target_quality = float(
        risk["target_quality"]
    )

    target_component = (
        target_quality *
        0.10
    )

    score += target_component

    # =====================================================
    # 8. Risk Quality = 5
    # =====================================================

    rr1 = float(
        risk["rr1"]
    )

    risk_pct_actual = float(
        risk["risk_pct"]
    )

    risk_score = 0

    if np.isfinite(rr1) and rr1 >= 2:
        risk_score += 3

    elif rr1 >= 1.5:
        risk_score += 2

    elif rr1 >= 1.2:
        risk_score += 1

    if risk_pct_actual <= 5:
        risk_score += 2

    elif risk_pct_actual <= 8:
        risk_score += 1

    score += min(
        5,
        risk_score
    )

    # =====================================================
    # EMA200 incomplete penalty
    # =====================================================

    incomplete_count = sum([
        not daily_ema200_complete,
        not weekly_ema200_complete,
        not monthly_ema200_complete
    ])

    if incomplete_count >= 2:
        score -= 4

    elif incomplete_count == 1:
        score -= 2

    # =====================================================
    # لا نعطي 85+ إذا كان Entry مجرد انتظار
    # =====================================================

    if entry_type == "انتظار تأكيد":

        score = min(
            score,
            69
        )

    # =====================================================
    # Final Score
    # =====================================================

    score = min(
        100,
        max(
            0,
            score
        )
    )

    # =====================================================
    # Confidence
    # =====================================================

    base_conf = ai_confidence(
        last_d,
        last_w,
        last_m,
        alignment,
        data_quality
    )

    (
        tp1_prob,
        tp2_prob,
        tp3_prob,
        tp4_prob
    ) = estimate_probabilities(
        base_conf,
        0 if not np.isfinite(risk["rr1"]) else risk["rr1"],
        0 if not np.isfinite(risk["rr2"]) else risk["rr2"],
        0 if not np.isfinite(risk["rr3"]) else risk["rr3"],
        0 if not np.isfinite(risk["rr4"]) else risk["rr4"],
        alignment,
        adx_val
    )

    # =====================================================
    # Signal
    # =====================================================

    if (
        score >= 85 and
        np.isfinite(rr1) and rr1 >= 1.5 and
        alignment >= 65 and
        entry_type != "انتظار تأكيد"
    ):

        signal = "🔥 قوي جداً"

    elif (
        score >= 70 and
        np.isfinite(rr1) and rr1 >= 1.3 and
        entry_type != "انتظار تأكيد"
    ):

        signal = "🟢 قوي"

    elif score >= 55:

        signal = "🟡 متوسط"

    else:

        signal = "⚠️ متابعة"

    # =====================================================
    # المدة المتوقعة
    # =====================================================

    volatility = (
        float(last_d["atr"]) /
        entry
    )

    if volatility > 0.07:
        time_est = "1 - 3 أسابيع"

    elif volatility > 0.04:
        time_est = "3 - 8 أسابيع"

    elif volatility > 0.02:
        time_est = "1 - 3 شهور"

    else:
        time_est = "2 - 4 شهور"

    # =====================================================
    # النتيجة
    # =====================================================

    return {

        "التقييم": round(
            score,
            2
        ),

        "نسبة الشراء %": buy_percentage,

        "الإشارة": signal,

        "الاتجاه": regime,

        "نوع الدخول": entry_type,

        "سبب الدخول": entry_reason,

        "سعر الدخول": round(
            entry,
            2
        ),

        "وقف الخسارة": round(
            stop,
            2
        ),

        "الهدف الأول": round(
            tp1,
            2
        ),

        "الهدف الثاني": round(
            tp2,
            2
        ),

        "الهدف الثالث": round(
            tp3,
            2
        ),

        "الهدف الرابع": round(
            tp4,
            2
        ),

        "سبب الهدف الأول": risk[
            "tp1_reason"
        ],

        "سبب الهدف الثاني": risk[
            "tp2_reason"
        ],

        "سبب الهدف الثالث": risk[
            "tp3_reason"
        ],

        "سبب الهدف الرابع": risk[
            "tp4_reason"
        ],

        "نوع الهدف الأول": risk[
            "tp1_category"
        ],

        "نوع الهدف الثاني": risk[
            "tp2_category"
        ],

        "نوع الهدف الثالث": risk[
            "tp3_category"
        ],

        "نوع الهدف الرابع": risk[
            "tp4_category"
        ],

        "ربح الهدف الأول %": round(
            risk["tp1_profit_pct"],
            2
        ),

        "ربح الهدف الثاني %": round(
            risk["tp2_profit_pct"],
            2
        ),

        "ربح الهدف الثالث %": round(
            risk["tp3_profit_pct"],
            2
        ),

        "ربح الهدف الرابع %": round(
            risk["tp4_profit_pct"],
            2
        ),

        "R/R الهدف الأول": round(
            risk["rr1"],
            2
        ),

        "R/R الهدف الثاني": round(
            risk["rr2"],
            2
        ),

        "R/R الهدف الثالث": round(
            risk["rr3"],
            2
        ),

        "R/R الهدف الرابع": round(
            risk["rr4"],
            2
        ),

        "ثقة الهدف الأول %": round(
            tp1_prob * 100,
            1
        ),

        "ثقة الهدف الثاني %": round(
            tp2_prob * 100,
            1
        ),

        "ثقة الهدف الثالث %": round(
            tp3_prob * 100,
            1
        ),

        "ثقة الهدف الرابع %": round(
            tp4_prob * 100,
            1
        ),

        "جودة الأهداف": round(
            target_quality,
            1
        ),

        "EMA200": ema200_status,

        "التذبذب ATR %": round(
            volatility * 100,
            2
        ),

        "قوة الاتجاه ADX": round(
            adx_val,
            2
        ),

        "مؤشر RSI": round(
            rsi,
            2
        ),

        "المدة المتوقعة": time_est,
        "السيولة Ratio": round(liquidity_ratio, 2),
        "قوة السيولة": round(liquidity_score + rs_score, 2),
        "Relative Strength %": round(relative_strength * 100, 2),
        "عدد الأهداف الهيكلية": int(risk.get("structural_target_count", 0)),

        # =================================================
        # معلومات داخلية
        # =================================================

        "_entry_type": entry_type,

        "_trend_alignment": round(
            alignment,
            2
        ),

        "_data_quality": round(
            data_quality,
            2
        ),

        "_ema200_daily": (
            "مكتمل"
            if daily_ema200_complete
            else "غير مكتمل"
        ),

        "_ema200_weekly": (
            "مكتمل"
            if weekly_ema200_complete
            else "غير مكتمل"
        ),

        "_ema200_monthly": (
            "مكتمل"
            if monthly_ema200_complete
            else "غير مكتمل"
        ),

        "_risk_pct": round(
            risk["risk_pct"],
            2
        ),

        "_rr1": round(
            risk["rr1"],
            2
        ),

        "_rr2": round(
            risk["rr2"],
            2
        ),

        "_rr3": round(
            risk["rr3"],
            2
        ),

        "_rr4": round(
            risk["rr4"],
            2
        ),

        "_target_quality": round(
            target_quality,
            2
        ),

        "_position_size": round(
            risk["position_size"],
            2
        ),

        "_position_value": round(
            risk["position_value"],
            2
        ),

        "_obv": round(
            obv,
            2
        ),

        "_obv_ma": round(
            obv_ma,
            2
        ),

        "_stoch_rsi_k": round(
            stoch_k,
            4
        ),

        "_stoch_rsi_d": round(
            stoch_d,
            4
        ),

        "_vwap": round(
            float(last_d["vwap"]),
            4
        ),

        "_pullback_quality": round(
            float(
                last_d.get(
                    "pullback_quality_score",
                    0
                )
            ),
            2
        ),

        "_volume_ratio": round(
            volume_ratio,
            2
        ),
        "_liquidity_ratio": round(liquidity_ratio, 2),
        "_relative_strength": round(relative_strength * 100, 2),
        "_structural_target_count": int(risk.get("structural_target_count", 0))
    }


# =========================================================
# 🧪 V9 REALISTIC HISTORICAL BACKTEST / VALIDATION ENGINE
# =========================================================
def _bt_signal(row):
    """Signal logic shared by the V9 backtest. Only signal-bar information."""
    try:
        close=float(row["Close"]); ema20=float(row["ema20"]); ema50=float(row["ema50"])
        rsi=float(row["rsi"]); macd=float(row["macd"]); macd_signal=float(row["macd_signal"])
        vol_ratio=float(row["volume_ratio"]); body_pct=float(row["body_pct"]); atr_pct=float(row["atr_pct"])
    except Exception:
        return False
    if not all(np.isfinite(x) for x in [close,ema20,ema50,rsi,macd,macd_signal,vol_ratio,body_pct,atr_pct]):
        return False
    breakout=bool(row.get("breakout",False))
    pullback=bool(row.get("pullback",False))
    immediate=(close>ema20>ema50 and rsi>=50 and macd>macd_signal and vol_ratio>=1.0 and 0.015<=atr_pct<=0.12)
    try: prev_res=float(row.get("previous_resistance",np.nan))
    except Exception: prev_res=np.nan
    breakout_fallback=np.isfinite(prev_res) and close>prev_res and vol_ratio>=1.30 and body_pct>=0.35 and close>ema20>ema50 and 0.015<=atr_pct<=0.12
    pullback_fallback=(close>ema20>ema50 and (abs(close-ema20)/close<=0.03 or abs(close-ema50)/close<=0.05) and rsi>=45 and macd>=macd_signal)
    return bool(breakout or pullback or immediate or breakout_fallback or pullback_fallback)


def _bt_structural_targets(row, entry):
    vals=[]
    for col,name in [
        ("previous_resistance","مقاومة يومية سابقة"),("resistance","مقاومة يومية"),
        ("confirmed_swing_high","آخر Swing High مؤكد"),("fib_ext_1272","Fib 127.2%"),
        ("fib_ext_1618","Fib 161.8%"),("fib_ext_2000","Fib 200%")]:
        try:
            x=float(row.get(col,np.nan))
            if np.isfinite(x) and x>entry*1.001: vals.append((x,name))
        except Exception: pass
    vals=sorted(vals,key=lambda z:z[0])
    out=[]
    for x,name in vals:
        if not out or abs(x-out[-1][0])/max(out[-1][0],1e-9)>=0.008:
            out.append((x,name))
        if len(out)>=4: break
    return out


def _simulate_bt_window(df, start_idx, end_idx, commission_pct=0.15, slippage_pct=0.10):
    trades=[]; equity=1.0; peak=1.0; max_dd=0.0; next_allowed=start_idx
    signals=entries=skipped_no_target=skipped_bad_stop=0
    warmup=max(BACKTEST_WARMUP,220)
    for i in range(max(start_idx,warmup), min(end_idx,len(df)-2)):
        if i<next_allowed: continue
        row=df.iloc[i]; signals+=1
        try:
            needed=["Open","High","Low","Close","ema20","ema50","rsi","macd","macd_signal","atr","volume_ratio","body_pct","atr_pct"]
            if not all(np.isfinite(float(row.get(c,np.nan))) for c in needed): continue
            atr_val=float(row["atr"]); close=float(row["Close"])
            if atr_val<=0 or close<=0 or not _bt_signal(row): continue
            raw_entry=float(df.iloc[i+1]["Open"])
            if not np.isfinite(raw_entry) or raw_entry<=0: continue
            # Buy-side execution cost: worse fill.
            entry=raw_entry*(1+slippage_pct/100.0+commission_pct/100.0)
            entries+=1
            try: swing=float(row.get("confirmed_swing_low",np.nan))
            except Exception: swing=np.nan
            if np.isfinite(swing) and 0<swing<entry:
                stop=max(swing-atr_val*0.20, entry-atr_val*1.50)
            else: stop=entry-atr_val*1.50
            if not np.isfinite(stop) or stop<=0 or stop>=entry:
                skipped_bad_stop+=1; continue
            targets=_bt_structural_targets(row,entry)
            # V9 STRICT: no ATR target fallback. No structural target = no trade.
            if not targets:
                skipped_no_target+=1; continue
            tprices=[x[0] for x in targets]
            # Partial exits: 25% at each available target. Remainder exits on trailing stop / final close.
            remaining=1.0; realized=0.0; tp_hits=0; exit_i=None
            trail=stop
            for j in range(i+1,min(end_idx,len(df))):
                bar=df.iloc[j]
                try: low=float(bar["Low"]); high=float(bar["High"]); close_j=float(bar["Close"])
                except Exception: continue
                # Conservative OHLC assumption: stop wins ties.
                if low<=trail:
                    exit_raw=trail*(1-slippage_pct/100.0-commission_pct/100.0)
                    realized += remaining*((exit_raw-entry)/entry); remaining=0; exit_i=j; break
                while tp_hits<len(tprices) and high>=tprices[tp_hits]:
                    qty=min(0.25,remaining)
                    exit_raw=tprices[tp_hits]*(1-slippage_pct/100.0-commission_pct/100.0)
                    realized += qty*((exit_raw-entry)/entry)
                    remaining-=qty; tp_hits+=1
                    # Progressive trailing: break-even after TP1, then prior-bar low / ATR trail.
                    if tp_hits==1: trail=max(trail,entry)
                    else: trail=max(trail,float(bar["Low"]), close_j-atr_val*1.5)
                if remaining<=1e-9:
                    exit_i=j; break
                # trailing update only after a confirmed target hit
                if tp_hits>0:
                    trail=max(trail,close_j-atr_val*1.5)
            if remaining>1e-9:
                j=min(end_idx-1,len(df)-1)
                exit_raw=float(df.iloc[j]["Close"])*(1-slippage_pct/100.0-commission_pct/100.0)
                realized += remaining*((exit_raw-entry)/entry); exit_i=j
            ret=float(realized)
            equity*=max(0.0001,1+ret); peak=max(peak,equity); max_dd=max(max_dd,(peak-equity)/peak)
            trades.append({"return":ret,"tp_hits":tp_hits,"bars":int(exit_i-i),"entry":entry})
            next_allowed=max(next_allowed,int(exit_i)+1)
        except Exception:
            continue
    return trades,equity,max_dd,signals,entries,skipped_no_target,skipped_bad_stop


def _summarize_bt(trades,equity,max_dd,signals,entries,skipped_no_target,skipped_bad_stop):
    rets=np.array([t["return"] for t in trades],dtype=float) if trades else np.array([],dtype=float)
    wins=rets[rets>0]; losses=rets[rets<0]
    gross_win=float(wins.sum()) if len(wins) else 0.0; gross_loss=float(abs(losses.sum())) if len(losses) else 0.0
    pf=(gross_win/gross_loss) if gross_loss>0 else (999.0 if gross_win>0 else 0.0)
    expectancy=float(rets.mean()) if len(rets) else 0.0
    std=float(rets.std(ddof=1)) if len(rets)>1 else 0.0
    sharpe=(expectancy/std*np.sqrt(len(rets))) if std>0 else 0.0
    downside=rets[rets<0]
    downside_std=float(downside.std(ddof=1)) if len(downside)>1 else 0.0
    sortino=(expectancy/downside_std*np.sqrt(len(rets))) if downside_std>0 else 0.0
    cagr=equity**(252/max(1,sum(t["bars"] for t in trades)))-1 if equity>0 and trades else 0.0
    calmar=(cagr/max_dd) if max_dd>0 else 0.0
    return {"trades":len(trades),"closed_trades":len(trades),"open_trades":0,
            "win_rate":(len(wins)/len(rets)*100 if len(rets) else 0.0),"profit_pct":(equity-1)*100,
            "max_drawdown_pct":max_dd*100,"profit_factor":pf,"avg_trade_pct":expectancy*100,
            "expectancy_pct":expectancy*100,"avg_win_pct":(wins.mean()*100 if len(wins) else 0),
            "avg_loss_pct":(losses.mean()*100 if len(losses) else 0),"sharpe":sharpe,"sortino":sortino,
            "calmar":calmar,"signals":signals,"entries":entries,"skipped_no_target":skipped_no_target,
            "skipped_bad_stop":skipped_bad_stop,"tp1_hit_rate":(sum(t["tp_hits"]>=1 for t in trades)/len(trades)*100 if trades else 0),
            "tp2_hit_rate":(sum(t["tp_hits"]>=2 for t in trades)/len(trades)*100 if trades else 0),
            "tp3_hit_rate":(sum(t["tp_hits"]>=3 for t in trades)/len(trades)*100 if trades else 0),
            "tp4_hit_rate":(sum(t["tp_hits"]>=4 for t in trades)/len(trades)*100 if trades else 0),
            "bars_used":sum(t["bars"] for t in trades) if trades else 0}


def run_real_backtest(df, max_bars=300, commission_pct=None, slippage_pct=None, monte_carlo_runs=500):
    empty={"trades":0,"closed_trades":0,"open_trades":0,"win_rate":0.0,"profit_pct":0.0,"max_drawdown_pct":0.0,"profit_factor":0.0,"avg_trade_pct":0.0,"expectancy_pct":0.0,"avg_win_pct":0.0,"avg_loss_pct":0.0,"sharpe":0.0,"sortino":0.0,"calmar":0.0,"signals":0,"entries":0,"skipped_no_target":0,"skipped_bad_stop":0,"bars_used":0,"tp1_hit_rate":0.0,"tp2_hit_rate":0.0,"tp3_hit_rate":0.0,"tp4_hit_rate":0.0,"monte_carlo_5pct":0.0,"monte_carlo_median":0.0,"monte_carlo_95pct":0.0,"walk_forward_score":0.0,"oos_return_pct":0.0}
    if df is None or df.empty: return empty
    try: bt=add_indicators(df.copy())
    except Exception: return empty
    if bt.empty: return empty
    comm=DEFAULT_COMMISSION_PCT if commission_pct is None else float(commission_pct)
    slip=DEFAULT_SLIPPAGE_PCT if slippage_pct is None else float(slippage_pct)
    warmup=max(BACKTEST_WARMUP,220); test_bars=max(50,int(max_bars)); start=max(warmup,len(bt)-test_bars-1); end=len(bt)-1
    trades,equity,dd,signals,entries,snt,sbs=_simulate_bt_window(bt,start,end,comm,slip)
    out=_summarize_bt(trades,equity,dd,signals,entries,snt,sbs); out["bars_used"]=max(0,end-start)
    # Monte Carlo on trade returns: distribution of terminal equity.
    if trades and monte_carlo_runs:
        rng=np.random.default_rng(42); r=np.array([t["return"] for t in trades],float); sims=[]
        for _ in range(int(monte_carlo_runs)):
            sample=rng.choice(r,size=len(r),replace=True); sims.append(float(np.prod(np.maximum(0.0001,1+sample))-1)*100)
        out["monte_carlo_5pct"]=float(np.percentile(sims,5)); out["monte_carlo_median"]=float(np.percentile(sims,50)); out["monte_carlo_95pct"]=float(np.percentile(sims,95))
    # Walk-forward / OOS: three chronological test windows, fixed strategy (no future fitting).
    n=len(bt); window=max(50,min(test_bars,n//5)); oos=[]
    for k in range(3):
        e=n-k*window; st_idx=max(warmup,e-window)
        if e-st_idx<50: continue
        tr,eq,dd2,sg,en,sn,sb=_simulate_bt_window(bt,st_idx,e,comm,slip)
        if tr: oos.append((eq-1)*100)
    if oos:
        out["oos_return_pct"]=float(np.mean(oos)); out["walk_forward_score"]=float(sum(x>0 for x in oos)/len(oos)*100)
    return out


def estimate_historical_probabilities(bt):
    return tuple(bt.get(k,0.0)/100.0 for k in ["tp1_hit_rate","tp2_hit_rate","tp3_hit_rate","tp4_hit_rate"])


def _clip_score(value, low, high):
    """تحويل قيمة رقمية إلى درجة 0-100 بشكل محافظ."""
    try:
        x = float(value)
    except Exception:
        return np.nan
    if not np.isfinite(x):
        return np.nan
    if high <= low:
        return 50.0
    return float(np.clip((x - low) / (high - low) * 100.0, 0.0, 100.0))


def calculate_trading_rank(row, backtest_enabled=True):
    """ترتيب تداولي مستقل عن التقييم الفني، مع استخدام نتائج الباك تست عند توفرها."""
    components = []

    def add(value, weight):
        if value is not None and np.isfinite(float(value)):
            components.append((float(np.clip(value, 0, 100)), float(weight)))

    # 35% جودة الإشارة الفنية الأساسية
    add(row.get("التقييم", np.nan), 35.0)

    if backtest_enabled:
        trades = row.get("Backtest Trades", np.nan)
        try:
            trades = float(trades)
        except Exception:
            trades = np.nan

        # نستخدم نتائج الباك تست فقط عندما يكون لها عدد صفقات معقول.
        if np.isfinite(trades) and trades >= 10:
            add(row.get("احتمال TP1 التاريخي %", np.nan), 15.0)
            add(_clip_score(row.get("قيمة متوقعة %", np.nan), -2.0, 5.0), 15.0)
            add(_clip_score(row.get("R/R الهدف الأول", np.nan), 0.8, 4.0), 10.0)
            add(row.get("جودة الأهداف", np.nan), 5.0)
            add(row.get("السيولة Ratio", np.nan) if np.isfinite(float(row.get("السيولة Ratio", np.nan))) else np.nan, 2.5)
            add(row.get("Walk Forward Score %", np.nan), 5.0)
            add(_clip_score(row.get("OOS Return %", np.nan), -20.0, 40.0), 5.0)
            # عقوبة خفيفة للـ Drawdown المرتفع، بعد تحويله إلى جودة.
            dd_quality = _clip_score(row.get("Backtest Max DD %", np.nan), 0.0, 30.0)
            if np.isfinite(dd_quality):
                add(100.0 - dd_quality, 2.5)
        else:
            # لو البيانات غير كافية، لا نعطيها وزنًا وهميًا.
            add(row.get("جودة الأهداف", np.nan), 10.0)
            add(_clip_score(row.get("R/R الهدف الأول", np.nan), 0.8, 4.0), 10.0)
            add(row.get("السيولة Ratio", np.nan) if np.isfinite(float(row.get("السيولة Ratio", np.nan))) else np.nan, 5.0)
    else:
        add(row.get("جودة الأهداف", np.nan), 20.0)
        add(_clip_score(row.get("R/R الهدف الأول", np.nan), 0.8, 4.0), 15.0)
        add(row.get("السيولة Ratio", np.nan) if np.isfinite(float(row.get("السيولة Ratio", np.nan))) else np.nan, 15.0)

    if not components:
        return 0.0
    return round(sum(v*w for v,w in components) / sum(w for _,w in components), 2)


def apply_trading_ranking(df, backtest_enabled=True):
    """إضافة الترتيب التداولي وفرز الأسهم من الأقوى للأضعف."""
    out = df.copy()
    if out.empty:
        return out
    out["الترتيب التداولي"] = out.apply(
        lambda r: calculate_trading_rank(r, backtest_enabled), axis=1
    )
    out = out.sort_values(
        ["الترتيب التداولي", "التقييم"],
        ascending=[False, False]
    ).reset_index(drop=True)
    out["الترتيب"] = np.arange(1, len(out) + 1)
    return out




# =========================================================
# ⚡ معالجة سهم واحد
# =========================================================

def process(
    symbol,
    daily,
    weekly,
    monthly,
    capital,
    risk_percent,
    market_return_20=0.0,
    run_backtest=False,
    backtest_bars=300
):

    clean_symbol = symbol.replace(
        ".CA",
        ""
    )

    try:

        df_d = extract_symbol_data(
            daily,
            symbol
        )

        df_w = extract_symbol_data(
            weekly,
            symbol
        )

        df_m = extract_symbol_data(
            monthly,
            symbol
        )

        if df_d.empty:

            return {
                "السهم": clean_symbol,
                "الحالة": "❌ لا توجد بيانات يومية"
            }

        if len(df_d) < MIN_DAILY_ROWS:

            return {
                "السهم": clean_symbol,
                "الحالة": "❌ بيانات يومية غير كافية"
            }

        if df_w.empty:

            return {
                "السهم": clean_symbol,
                "الحالة": "❌ لا توجد بيانات أسبوعية"
            }

        if len(df_w) < MIN_WEEKLY_ROWS:

            return {
                "السهم": clean_symbol,
                "الحالة": "❌ بيانات أسبوعية غير كافية"
            }

        if df_m.empty:

            return {
                "السهم": clean_symbol,
                "الحالة": "❌ لا توجد بيانات شهرية"
            }

        if len(df_m) < MIN_MONTHLY_ROWS:

            return {
                "السهم": clean_symbol,
                "الحالة": "❌ بيانات شهرية غير كافية"
            }

        # تاريخ آخر شمعة يومية تم جلبها فعليًا
        last_candle_date = pd.Timestamp(
            df_d.index[-1]
        ).strftime("%Y-%m-%d")

        df_d["market_return_20"] = market_return_20
        result = analyze(
            df_d,
            df_w,
            df_m,
            capital,
            risk_percent
        )
        result["تاريخ آخر شمعة Close"] = last_candle_date
        if run_backtest:
            bt = run_real_backtest(df_d, backtest_bars, commission_pct, slippage_pct, monte_carlo_runs)
            result["Backtest Trades"] = bt["trades"]
            result["Backtest Win Rate %"] = round(bt["win_rate"], 1)
            result["Backtest Return %"] = round(bt["profit_pct"], 2)
            result["Backtest Max DD %"] = round(bt["max_drawdown_pct"], 2)
            result["Backtest Profit Factor"] = round(bt["profit_factor"], 2)
            result["Backtest Signals"] = int(bt.get("signals", 0))
            result["Backtest Valid Entries"] = int(bt.get("entries", 0))
            result["Backtest No Target"] = int(bt.get("skipped_no_target", 0))
            result["Backtest Bad Stop"] = int(bt.get("skipped_bad_stop", 0))
            result["Backtest Invalid Indicators"] = 0
            result["Backtest Expectancy %"] = round(bt.get("expectancy_pct",0.0),3)
            result["Backtest Avg Win %"] = round(bt.get("avg_win_pct",0.0),2)
            result["Backtest Avg Loss %"] = round(bt.get("avg_loss_pct",0.0),2)
            result["Backtest Sharpe"] = round(bt.get("sharpe",0.0),2)
            result["Backtest Sortino"] = round(bt.get("sortino",0.0),2)
            result["Backtest Calmar"] = round(bt.get("calmar",0.0),2)
            result["Backtest TP1 Probability %"] = round(bt.get("tp1_hit_rate",0.0),1)
            result["Backtest TP2 Probability %"] = round(bt.get("tp2_hit_rate",0.0),1)
            result["Backtest TP3 Probability %"] = round(bt.get("tp3_hit_rate",0.0),1)
            result["Backtest TP4 Probability %"] = round(bt.get("tp4_hit_rate",0.0),1)
            result["Monte Carlo 5% Return %"] = round(bt.get("monte_carlo_5pct",0.0),2)
            result["Monte Carlo Median Return %"] = round(bt.get("monte_carlo_median",0.0),2)
            result["Monte Carlo 95% Return %"] = round(bt.get("monte_carlo_95pct",0.0),2)
            result["Walk Forward Score %"] = round(bt.get("walk_forward_score",0.0),1)
            result["OOS Return %"] = round(bt.get("oos_return_pct",0.0),2)
            # V9: historical probabilities replace synthetic confidence for trading decisions.
            result["احتمال TP1 التاريخي %"] = round(bt.get("tp1_hit_rate",0.0),1)
            result["احتمال TP2 التاريخي %"] = round(bt.get("tp2_hit_rate",0.0),1)
            result["احتمال TP3 التاريخي %"] = round(bt.get("tp3_hit_rate",0.0),1)
            result["احتمال TP4 التاريخي %"] = round(bt.get("tp4_hit_rate",0.0),1)
            result["قيمة متوقعة %"] = round(bt.get("expectancy_pct",0.0),3)
            result["حالة التحقق"] = ("🟢 قوي" if bt.get("walk_forward_score",0)>=66 and bt.get("expectancy_pct",0)>0 and bt.get("profit_factor",0)>1.1 else "🟡 محايد" if bt.get("trades",0)>=10 else "⚪ بيانات غير كافية")
        else:
            result["Backtest Trades"] = 0
            result["Backtest Win Rate %"] = np.nan
            result["Backtest Return %"] = np.nan
            result["Backtest Max DD %"] = np.nan
            result["Backtest Profit Factor"] = np.nan
            result["Backtest Signals"] = np.nan
            result["Backtest Valid Entries"] = np.nan
            result["Backtest No Target"] = np.nan
            result["Backtest Bad Stop"] = np.nan
            result["Backtest Invalid Indicators"] = np.nan
            for _k in ["Backtest Expectancy %","Backtest Avg Win %","Backtest Avg Loss %","Backtest Sharpe","Backtest Sortino","Backtest Calmar","Backtest TP1 Probability %","Backtest TP2 Probability %","Backtest TP3 Probability %","Backtest TP4 Probability %","Monte Carlo 5% Return %","Monte Carlo Median Return %","Monte Carlo 95% Return %","Walk Forward Score %","OOS Return %","احتمال TP1 التاريخي %","احتمال TP2 التاريخي %","احتمال TP3 التاريخي %","احتمال TP4 التاريخي %","قيمة متوقعة %"]: result[_k]=np.nan
            result["حالة التحقق"]="⚪ Backtest غير مفعل"

        result["السهم"] = clean_symbol
        result["الحالة"] = "✅ تم التحليل"

        return result

    except Exception as e:

        return {
            "السهم": clean_symbol,
            "الحالة": f"❌ {str(e)[:120]}"
        }


# =========================================================
# 💼 إدارة المحفظة: تداول + استثمار (Excel/CSV)
# =========================================================

PORTFOLIO_TX_COLUMNS = ["التاريخ", "نوع العملية", "السهم", "الكمية", "السعر", "العمولة", "ملاحظات"]
PORTFOLIO_PRICE_COLUMNS = ["السهم", "السعر الحالي", "ملاحظات"]
PORTFOLIO_ACTIONS = ["شراء تداول", "بيع تداول", "شراء استثمار", "بيع استثمار", "توزيع نقدي", "إيداع نقدي", "سحب نقدي", "منحة أسهم"]


def _portfolio_empty_transactions():
    return pd.DataFrame(columns=PORTFOLIO_TX_COLUMNS)


def _portfolio_empty_prices():
    return pd.DataFrame(columns=PORTFOLIO_PRICE_COLUMNS)


def _portfolio_clean_transactions(frame):
    frame = frame.copy()
    for col in PORTFOLIO_TX_COLUMNS:
        if col not in frame.columns:
            frame[col] = "" if col in ["التاريخ", "نوع العملية", "السهم", "ملاحظات"] else 0.0
    frame = frame[PORTFOLIO_TX_COLUMNS]
    frame["التاريخ"] = pd.to_datetime(frame["التاريخ"], errors="coerce", dayfirst=True).dt.strftime("%Y-%m-%d")
    frame["نوع العملية"] = frame["نوع العملية"].fillna("").astype(str).str.strip()
    frame["السهم"] = frame["السهم"].fillna("").astype(str).str.upper().str.strip()
    for col in ["الكمية", "السعر", "العمولة"]:
        frame[col] = pd.to_numeric(frame[col], errors="coerce").fillna(0.0)
    frame["ملاحظات"] = frame["ملاحظات"].fillna("").astype(str)
    return frame


def _portfolio_clean_prices(frame):
    frame = frame.copy()
    for col in PORTFOLIO_PRICE_COLUMNS:
        if col not in frame.columns:
            frame[col] = "" if col != "السعر الحالي" else 0.0
    frame = frame[PORTFOLIO_PRICE_COLUMNS]
    frame["السهم"] = frame["السهم"].fillna("").astype(str).str.upper().str.strip()
    frame["السعر الحالي"] = pd.to_numeric(frame["السعر الحالي"], errors="coerce")
    frame["ملاحظات"] = frame["ملاحظات"].fillna("").astype(str)
    return frame


def _portfolio_calculate(transactions, prices):
    tx = _portfolio_clean_transactions(transactions)
    tx = tx[tx["نوع العملية"].isin(PORTFOLIO_ACTIONS)].copy()
    tx = tx.sort_values(["التاريخ"], na_position="last", kind="stable")
    positions = {}
    cash_flow = 0.0
    realized = 0.0
    realized_trade = 0.0
    realized_invest = 0.0
    dividends = 0.0
    deposits = 0.0
    withdrawals = 0.0
    invalid = 0
    for _, row in tx.iterrows():
        action, sym = row["نوع العملية"], row["السهم"]
        qty, price, fee = float(row["الكمية"]), float(row["السعر"]), float(row["العمولة"])
        if action in ["إيداع نقدي", "سحب نقدي"]:
            amount = qty if qty > 0 else price
            if action == "إيداع نقدي": deposits += amount; cash_flow += amount
            else: withdrawals += amount; cash_flow -= amount
            continue
        if action == "توزيع نقدي":
            amount = qty * price if qty > 0 and price > 0 else price
            dividends += amount
            cash_flow += amount - fee
            continue
        if action == "منحة أسهم":
            if not sym or qty <= 0: invalid += 1; continue
            bucket = "استثمار"
            pos = positions.setdefault((sym, bucket), {"qty": 0.0, "cost": 0.0, "realized": 0.0})
            pos["qty"] += qty
            continue
        if not sym or qty <= 0 or price < 0:
            invalid += 1; continue
        bucket = "تداول" if action in ["شراء تداول", "بيع تداول"] else "استثمار"
        pos = positions.setdefault((sym, bucket), {"qty": 0.0, "cost": 0.0, "realized": 0.0})
        gross = qty * price
        if action in ["شراء تداول", "شراء استثمار"]:
            pos["qty"] += qty
            pos["cost"] += gross + fee
            cash_flow -= gross + fee
        elif action in ["بيع تداول", "بيع استثمار"]:
            if qty > pos["qty"] + 1e-8:
                invalid += 1
                continue
            avg_cost = pos["cost"] / pos["qty"] if pos["qty"] > 0 else 0.0
            pnl = gross - fee - avg_cost * qty
            pos["qty"] -= qty
            pos["cost"] -= avg_cost * qty
            pos["realized"] += pnl
            realized += pnl
            if bucket == "تداول": realized_trade += pnl
            else: realized_invest += pnl
            cash_flow += gross - fee
    price_map = {}
    px = _portfolio_clean_prices(prices)
    if not px.empty:
        px = px.dropna(subset=["السعر الحالي"]).drop_duplicates("السهم", keep="last")
        price_map = dict(zip(px["السهم"], px["السعر الحالي"]))
    holdings = []
    market_value_total = 0.0
    cost_total = 0.0
    unrealized_total = 0.0
    for (sym, bucket), pos in positions.items():
        qty = max(0.0, pos["qty"])
        if qty <= 1e-8: continue
        cost = max(0.0, pos["cost"])
        avg = cost / qty if qty else 0.0
        current = price_map.get(sym, np.nan)
        market_value = qty * current if pd.notna(current) else np.nan
        unrealized = market_value - cost if pd.notna(market_value) else np.nan
        if pd.notna(market_value): market_value_total += market_value
        cost_total += cost
        if pd.notna(unrealized): unrealized_total += unrealized
        holdings.append({"التصنيف": bucket, "السهم": sym, "الكمية الحالية": qty, "متوسط التكلفة": avg, "إجمالي التكلفة": cost,
                         "السعر الحالي": current, "القيمة السوقية": market_value,
                         "ربح/خسارة غير محققة": unrealized, "ربح/خسارة محققة": pos["realized"]})
    hdf = pd.DataFrame(holdings)
    if not hdf.empty: hdf = hdf.sort_values("القيمة السوقية", ascending=False, na_position="last")
    return {"holdings": hdf, "cash": cash_flow, "realized": realized, "realized_trade": realized_trade,
            "realized_invest": realized_invest, "dividends": dividends, "deposits": deposits,
            "withdrawals": withdrawals, "market_value": market_value_total,
            "cost": cost_total, "unrealized": unrealized_total, "invalid": invalid}


if "portfolio_transactions" not in st.session_state:
    st.session_state.portfolio_transactions = _portfolio_empty_transactions()
if "portfolio_prices" not in st.session_state:
    st.session_state.portfolio_prices = _portfolio_empty_prices()

st.markdown("---")
st.header("💼 إدارة المحفظة الاستثمارية والتداول")
st.caption("سجل موحد للعمليات مع فصل نتائج التداول عن الاستثمار. استورد نسخة Excel كاملة أو ملف CSV للعمليات أو الأسعار. الحفظ الدائم يتم بتنزيل نسخة احتياطية والاحتفاظ بها خارج التطبيق.")

with st.expander("📥 استيراد محفظة أو استعادة نسخة احتياطية", expanded=False):
    uploaded_portfolio = st.file_uploader("ارفع نسخة Excel كاملة أو أحد ملفات CSV الاحتياطية", type=["csv", "xlsx"], key="portfolio_upload")
    if uploaded_portfolio is not None:
        upload_token = f"{uploaded_portfolio.name}:{uploaded_portfolio.size}"
        if st.session_state.get("portfolio_last_import_token") != upload_token:
            try:
                if uploaded_portfolio.name.lower().endswith(".csv"):
                    imported_csv = pd.read_csv(uploaded_portfolio)
                    if "السعر الحالي" in imported_csv.columns:
                        st.session_state.portfolio_prices = _portfolio_clean_prices(imported_csv)
                    else:
                        st.session_state.portfolio_transactions = _portfolio_clean_transactions(imported_csv)
                else:
                    from io import BytesIO
                    portfolio_xls = pd.ExcelFile(BytesIO(uploaded_portfolio.getvalue()), engine="openpyxl")
                    imported_tx = pd.read_excel(portfolio_xls, sheet_name="العمليات")
                    try: imported_prices = pd.read_excel(portfolio_xls, sheet_name="الأسعار الحالية")
                    except Exception: imported_prices = _portfolio_empty_prices()
                    st.session_state.portfolio_transactions = _portfolio_clean_transactions(imported_tx)
                    st.session_state.portfolio_prices = _portfolio_clean_prices(imported_prices)
                st.session_state.pop("portfolio_tx_editor", None)
                st.session_state.pop("portfolio_price_editor", None)
                st.session_state.portfolio_last_import_token = upload_token
                st.success("تم استيراد البيانات. راجع الجداول ثم نزّل نسخة احتياطية جديدة.")
            except Exception as exc:
                st.error(f"تعذر قراءة الملف: {str(exc)[:180]}")

left, right = st.columns([1.15, 1])
with left:
    st.subheader("🧾 سجل العمليات")
    st.caption("كل صف يمثل عملية واحدة. الشراء والبيع يُسجلان بالكمية والسعر والعمولة. للتوزيع النقدي: اكتب قيمة التوزيع في خانة السعر والكمية = 1.")
    edited_tx = st.data_editor(
        _portfolio_clean_transactions(st.session_state.portfolio_transactions),
        num_rows="dynamic", use_container_width=True, hide_index=True,
        column_config={
            "التاريخ": st.column_config.TextColumn("التاريخ", help="YYYY-MM-DD"),
            "نوع العملية": st.column_config.SelectboxColumn("نوع العملية", options=PORTFOLIO_ACTIONS, required=True),
            "السهم": st.column_config.TextColumn("السهم (.CA)", help="مثال: COMI.CA"),
            "الكمية": st.column_config.NumberColumn("الكمية / مبلغ الإيداع", min_value=0.0, step=1.0),
            "السعر": st.column_config.NumberColumn("السعر / مبلغ التوزيع", min_value=0.0, step=0.01),
            "العمولة": st.column_config.NumberColumn("العمولة", min_value=0.0, step=0.01),
        }, key="portfolio_tx_editor"
    )
    st.session_state.portfolio_transactions = _portfolio_clean_transactions(edited_tx)
with right:
    st.subheader("💹 أسعار التقييم الحالية")
    st.caption("أدخل آخر سعر إغلاق لكل سهم لمتابعة القيمة السوقية. السعر لا يُستخدم لتغيير تكلفة الشراء.")
    edited_prices = st.data_editor(
        _portfolio_clean_prices(st.session_state.portfolio_prices),
        num_rows="dynamic", use_container_width=True, hide_index=True,
        column_config={
            "السهم": st.column_config.TextColumn("السهم (.CA)"),
            "السعر الحالي": st.column_config.NumberColumn("آخر سعر إغلاق", min_value=0.0, step=0.01),
            "ملاحظات": st.column_config.TextColumn("مصدر / تاريخ السعر"),
        }, key="portfolio_price_editor"
    )
    st.session_state.portfolio_prices = _portfolio_clean_prices(edited_prices)

portfolio_result = _portfolio_calculate(st.session_state.portfolio_transactions, st.session_state.portfolio_prices)
p1, p2, p3, p4, p5 = st.columns(5)
p1.metric("قيمة الأسهم المسعّرة", f"{portfolio_result['market_value']:,.2f} ج")
p2.metric("النقدية المحسوبة", f"{portfolio_result['cash']:,.2f} ج")
p3.metric("ربح/خسارة غير محققة", f"{portfolio_result['unrealized']:,.2f} ج")
p4.metric("ربح/خسارة محققة", f"{portfolio_result['realized']:,.2f} ج")
p5.metric("التوزيعات النقدية", f"{portfolio_result['dividends']:,.2f} ج")

if portfolio_result["invalid"]:
    st.warning(f"يوجد {portfolio_result['invalid']} عملية غير صالحة أو بيع أكبر من الكمية المتاحة؛ راجع سجل العمليات.")
if not portfolio_result["holdings"].empty:
    unpriced_count = int(portfolio_result["holdings"]["السعر الحالي"].isna().sum())
    if unpriced_count:
        st.warning(f"هناك {unpriced_count} مركز بدون سعر حالي؛ قيمة الأسهم المعروضة جزئية وليست إجمالي قيمة المحفظة.")
if not portfolio_result["holdings"].empty:
    st.subheader("📊 المراكز الحالية")
    st.dataframe(portfolio_result["holdings"], use_container_width=True, hide_index=True)
else:
    st.info("أضف عمليات شراء لعرض المراكز الحالية. ابدأ بتسجيل الإيداع النقدي ثم عمليات الشراء.")

st.subheader("📈 فصل التداول عن الاستثمار")
trade_actions = ["شراء تداول", "بيع تداول"]
invest_actions = ["شراء استثمار", "بيع استثمار"]
tx_valid = _portfolio_clean_transactions(st.session_state.portfolio_transactions)
trade_rows = tx_valid[tx_valid["نوع العملية"].isin(trade_actions)]
invest_rows = tx_valid[tx_valid["نوع العملية"].isin(invest_actions)]
c1, c2 = st.columns(2)
with c1:
    st.markdown("**التداول**")
    st.metric("عدد عمليات التداول", len(trade_rows))
    st.metric("صافي الربح المحقق من التداول", f"{portfolio_result['realized_trade']:,.2f} ج")
    trade_unrealized = float(portfolio_result["holdings"].loc[portfolio_result["holdings"]["التصنيف"] == "تداول", "ربح/خسارة غير محققة"].fillna(0).sum()) if not portfolio_result["holdings"].empty else 0.0
    st.metric("ربح/خسارة غير محققة للتداول", f"{trade_unrealized:,.2f} ج")
with c2:
    st.markdown("**الاستثمار طويل الأجل**")
    st.metric("عدد عمليات الاستثمار", len(invest_rows))
    st.metric("صافي الربح المحقق من الاستثمار", f"{portfolio_result['realized_invest']:,.2f} ج")
    invest_unrealized = float(portfolio_result["holdings"].loc[portfolio_result["holdings"]["التصنيف"] == "استثمار", "ربح/خسارة غير محققة"].fillna(0).sum()) if not portfolio_result["holdings"].empty else 0.0
    st.metric("ربح/خسارة غير محققة للاستثمار", f"{invest_unrealized:,.2f} ج")

# Export: a multi-sheet Excel backup plus separate CSV files
try:
    from io import BytesIO
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
        _portfolio_clean_transactions(st.session_state.portfolio_transactions).to_excel(writer, sheet_name="العمليات", index=False)
        _portfolio_clean_prices(st.session_state.portfolio_prices).to_excel(writer, sheet_name="الأسعار الحالية", index=False)
        portfolio_result["holdings"].to_excel(writer, sheet_name="المراكز الحالية", index=False)
    excel_bytes = excel_buffer.getvalue()
    st.download_button("⬇️ تنزيل نسخة احتياطية كاملة Excel", excel_bytes, "EGX_Portfolio_Backup.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", key="portfolio_backup_xlsx")
except Exception as exc:
    st.warning(f"تعذر تجهيز ملف Excel؛ استخدم ملفات CSV أدناه. التفاصيل: {str(exc)[:120]}")

exp1, exp2 = st.columns(2)
with exp1:
    tx_csv = _portfolio_clean_transactions(st.session_state.portfolio_transactions).to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ تصدير سجل العمليات CSV", tx_csv, "EGX_Portfolio_Transactions.csv", "text/csv", key="portfolio_export_tx")
with exp2:
    px_csv = _portfolio_clean_prices(st.session_state.portfolio_prices).to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇️ تصدير الأسعار الحالية CSV", px_csv, "EGX_Portfolio_Prices.csv", "text/csv", key="portfolio_export_px")

st.caption("ملاحظات محاسبية: حساب متوسط تكلفة مرجّح زمنيًا، مع احتساب عمولات الشراء والبيع. المنحة تزيد عدد الأسهم دون زيادة التكلفة. لا تُسجل كسور الأسهم أو الضرائب تلقائيًا إلا بإدخالها ضمن العمولة. احفظ نسخة Excel بعد كل تحديث؛ ملفات Streamlit Cloud المحلية وبيانات الجلسة ليست تخزينًا دائمًا.")


# =========================================================
# 🚀 تشغيل الفحص
# =========================================================

if st.button(
    "🚀 بدء فحص الأسهم",
    use_container_width=True
):

    st.info(
        f"📡 جاري فحص {TOTAL_STOCKS} سهم..."
    )

    progress = st.progress(
        0
    )

    status_text = st.empty()

    # =====================================================
    # Daily
    # =====================================================

    with st.spinner(
        "📥 جاري تحميل البيانات اليومية..."
    ):

        daily = load_data(
            EGX100,
            period_daily,
            "1d"
        )

    progress.progress(
        20
    )

    # =====================================================
    # Weekly
    # =====================================================

    status_text.info(
        "📥 جاري تحميل البيانات الأسبوعية..."
    )

    weekly = load_data(
        EGX100,
        period_weekly,
        "1wk"
    )

    progress.progress(
        40
    )

    # =====================================================
    # Monthly
    # =====================================================

    status_text.info(
        "📥 جاري تحميل البيانات الشهرية..."
    )

    monthly = load_data(
        EGX100,
        period_monthly,
        "1mo"
    )

    progress.progress(
        50
    )

    # =====================================================
    # Data Engine Stats
    # =====================================================

    status_text.info(
        "🔍 جاري فحص جودة البيانات والتغطية..."
    )

    data_engine_stats = []

    for symbol in EGX100:

        df_d_check = extract_symbol_data(
            daily,
            symbol
        )

        df_w_check = extract_symbol_data(
            weekly,
            symbol
        )

        df_m_check = extract_symbol_data(
            monthly,
            symbol
        )

        qd = calculate_data_quality(
            df_d_check
        )

        qw = calculate_data_quality(
            df_w_check
        )

        qm = calculate_data_quality(
            df_m_check
        )

        quality = (
            qd["quality"] * 0.50 +
            qw["quality"] * 0.30 +
            qm["quality"] * 0.20
        )

        data_engine_stats.append({

            "symbol": symbol,

            "daily_rows":
                qd["rows"],

            "weekly_rows":
                qw["rows"],

            "monthly_rows":
                qm["rows"],

            "daily_quality":
                qd["quality"],

            "weekly_quality":
                qw["quality"],

            "monthly_quality":
                qm["quality"],

            "data_quality":
                round(
                    quality,
                    2
                ),

            "daily_ema200":
                (
                    "✅"
                    if qd["rows"] >= 200
                    else "⚠️"
                ),

            "weekly_ema200":
                (
                    "✅"
                    if qw["rows"] >= 200
                    else "⚠️"
                ),

            "monthly_ema200":
                (
                    "✅"
                    if qm["rows"] >= 200
                    else "⚠️"
                )
        })

    # =====================================================
    # Relative Strength market proxy
    # =====================================================
    market_return_20 = build_market_return_proxy(daily, EGX100)

    # =====================================================
    # التحليل
    # =====================================================

    results = []

    status_text.info(
        f"🧠 جاري تحليل {TOTAL_STOCKS} سهم بالتوازي..."
    )

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        futures = {

            executor.submit(
                process,
                symbol,
                daily,
                weekly,
                monthly,
                capital,
                risk_percent,
                market_return_20,
                run_backtest,
                backtest_bars
            ): symbol

            for symbol in EGX100
        }

        completed = 0

        for future in as_completed(
            futures
        ):

            try:

                result = future.result()

                if result:
                    results.append(
                        result
                    )

            except Exception as e:

                symbol = futures[
                    future
                ]

                results.append({

                    "السهم":
                        symbol.replace(
                            ".CA",
                            ""
                        ),

                    "الحالة":
                        f"❌ {str(e)[:120]}"
                })

            completed += 1

            progress.progress(
                50 +
                int(
                    completed /
                    TOTAL_STOCKS *
                    50
                )
            )

    progress.progress(
        100
    )

    status_text.success(
        "✅ انتهى الفحص بالكامل"
    )

    # =====================================================
    # النتائج
    # =====================================================

    if not results:

        st.error(
            "❌ لم يتم الحصول على أي نتائج."
        )

        st.stop()

    df_all = pd.DataFrame(
        results
    )

    financial_df = pd.DataFrame()
    if run_financial_scan:
        st.subheader("🏦 محرك التحليل المالي")
        with st.spinner("📚 جاري تحميل القوائم المالية السنوية وأسعار الإغلاق غير المعدلة..."):
            raw_financial_prices = load_raw_close_data(EGX100)
            financial_df = scan_financial_universe(
                EGX100, daily, raw_financial_prices, financial_workers,
                cost_of_equity_pct, base_growth_pct, terminal_growth_pct, target_pe_multiple
            )

    # =====================================================
    # الأسهم الناجحة
    # =====================================================

    df_ok = df_all[
        df_all["الحالة"] ==
        "✅ تم التحليل"
    ].copy()

    if not df_ok.empty and "عدد الأهداف الهيكلية" in df_ok.columns:
        no_targets = int((df_ok["عدد الأهداف الهيكلية"] < 1).sum())
        if no_targets:
            st.warning(f"⚠️ {no_targets} سهم بدون مستوى Target هيكلي موثوق؛ النظام لا يخترع أهداف ATR بديلة.")

    # =====================================================
    # التغطية
    # =====================================================

    total = TOTAL_STOCKS

    analyzed = int(
        (
            df_all["الحالة"] ==
            "✅ تم التحليل"
        ).sum()
    )

    failed = total - analyzed

    coverage = (
        analyzed /
        total *
        100
        if total > 0
        else 0
    )

    # =====================================================
    # Data Quality
    # =====================================================

    stats_df = pd.DataFrame(
        data_engine_stats
    )

    if not stats_df.empty:

        avg_quality = float(
            stats_df[
                "data_quality"
            ].mean()
        )

        daily_coverage = float(
            (
                stats_df[
                    "daily_rows"
                ] >= MIN_DAILY_ROWS
            ).mean() * 100
        )

        weekly_coverage = float(
            (
                stats_df[
                    "weekly_rows"
                ] >= MIN_WEEKLY_ROWS
            ).mean() * 100
        )

        monthly_coverage = float(
            (
                stats_df[
                    "monthly_rows"
                ] >= MIN_MONTHLY_ROWS
            ).mean() * 100
        )

        daily_ema200_coverage = float(
            (
                stats_df[
                    "daily_rows"
                ] >= 200
            ).mean() * 100
        )

        weekly_ema200_coverage = float(
            (
                stats_df[
                    "weekly_rows"
                ] >= 200
            ).mean() * 100
        )

        monthly_ema200_coverage = float(
            (
                stats_df[
                    "monthly_rows"
                ] >= 200
            ).mean() * 100
        )

    else:

        avg_quality = 0
        daily_coverage = 0
        weekly_coverage = 0
        monthly_coverage = 0
        daily_ema200_coverage = 0
        weekly_ema200_coverage = 0
        monthly_ema200_coverage = 0

    # =====================================================
    # ملخص الفحص
    # =====================================================

    st.subheader(
        "📊 ملخص الفحص"
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📊 الأسهم المطلوبة",
        total
    )

    c2.metric(
        "✅ تم تحليلها",
        analyzed
    )

    c3.metric(
        "❌ فشل",
        failed
    )

    c4.metric(
        "📡 نسبة التغطية",
        f"{coverage:.1f}%"
    )

    # =====================================================
    # جودة البيانات
    # =====================================================

    st.subheader(
        "📡 جودة البيانات"
    )

    q1, q2, q3, q4 = st.columns(4)

    q1.metric(
        "⭐ جودة البيانات",
        f"{avg_quality:.1f}%"
    )

    q2.metric(
        "📅 تغطية Daily",
        f"{daily_coverage:.1f}%"
    )

    q3.metric(
        "📆 تغطية Weekly",
        f"{weekly_coverage:.1f}%"
    )

    q4.metric(
        "🗓️ تغطية Monthly",
        f"{monthly_coverage:.1f}%"
    )

    st.subheader(
        "📐 تغطية EMA200 الحقيقي"
    )

    e1, e2, e3 = st.columns(3)

    e1.metric(
        "Daily EMA200",
        f"{daily_ema200_coverage:.1f}%"
    )

    e2.metric(
        "Weekly EMA200",
        f"{weekly_ema200_coverage:.1f}%"
    )

    e3.metric(
        "Monthly EMA200",
        f"{monthly_ema200_coverage:.1f}%"
    )

    # =====================================================
    # الأسهم الناجحة
    # =====================================================

    if not df_ok.empty:

        # ترتيب تداولي: لا يعتمد على Score الفني وحده، بل يدمج جودة الإشارة
        # مع نتائج الباك تست الواقعية عندما تكون متاحة.
        df_ok = apply_trading_ranking(
            df_ok,
            backtest_enabled=run_backtest
        )
        # =================================================
        # صفحة إشارات الدخول الفوري والاختراق وPullback
        # =================================================
        st.subheader("🚦 إشارات الدخول الفوري والاختراق وPullback")
        st.caption(
            "الإشارات مرتبة حسب الترتيب التداولي. الدخول الفوري بالأخضر، "
            "والاختراق بالأزرق، وPullback باللون البنفسجي. هذه إشارات ناتجة "
            "عن محرك Entry الحالي وليست توصية مضمونة بالتنفيذ."
        )

        signal_cols = [
            "الترتيب", "السهم", "التقييم", "الإشارة", "الاتجاه",
            "نوع الدخول", "سبب الدخول", "نسبة الشراء %", "سعر الدخول",
            "وقف الخسارة", "الهدف الأول", "ربح الهدف الأول %", "R/R الهدف الأول",
            "الهدف الثاني", "ربح الهدف الثاني %", "R/R الهدف الثاني",
            "جودة الأهداف", "مؤشر RSI", "قوة الاتجاه ADX", "التذبذب ATR %",
            "Backtest Trades", "Backtest Win Rate %", "حالة التحقق"
        ]
        signal_cols = [c for c in signal_cols if c in df_ok.columns]
        signal_tabs = st.tabs([
            "🟢 الدخول الفوري",
            "🔵 اختراق المقاومة",
            "🟣 دخول Pullback"
        ])
        signal_types = ["دخول فوري", "دخول اختراق", "دخول عند Pullback"]
        signal_colors = ["#16803c", "#1769aa", "#7540a5"]
        for signal_tab, signal_type, signal_color in zip(signal_tabs, signal_types, signal_colors):
            with signal_tab:
                signal_df = df_ok[df_ok["نوع الدخول"].astype(str) == signal_type].copy()
                if "الترتيب التداولي" in signal_df.columns:
                    signal_df = signal_df.sort_values("الترتيب التداولي", ascending=False)
                if signal_df.empty:
                    st.info(f"لا توجد حاليًا أسهم تحقق شروط: {signal_type}.")
                else:
                    st.markdown(
                        f"<div style='padding:8px 12px;border-right:5px solid {signal_color};'>"
                        f"عدد الأسهم المطابقة: <b>{len(signal_df)}</b></div>",
                        unsafe_allow_html=True
                    )
                    st.dataframe(
                        display_with_buy_percentage(signal_df[signal_cols]),
                        use_container_width=True,
                        hide_index=True
                    )
                    signal_csv = signal_df[signal_cols].to_csv(index=False).encode("utf-8-sig")
                    st.download_button(
                        f"⬇️ تحميل إشارات {signal_type}",
                        signal_csv,
                        f"EGX_{signal_type.replace(' ', '_')}_signals.csv",
                        "text/csv",
                        key=f"download_signal_{signal_type}"
                    )

        # =================================================
        # أفضل الأسهم
        # =================================================

        st.subheader(
            f"🏆 أفضل {min(top_n, len(df_ok))} سهم"
        )

        top_df = df_ok.head(
            top_n
        ).copy()

        preferred_cols = [

            "الترتيب",
            "السهم",
            "الترتيب التداولي",
            "التقييم المالي",
            "الدرجة الاستثمارية",
            "الترتيب الاستثماري",
            "التقييم",
            "نسبة الشراء %",
            "الإشارة",
            "الاتجاه",
            "نوع الدخول",
            "سبب الدخول",
            "سعر الدخول",
            "وقف الخسارة",

            "الهدف الأول",
            "ربح الهدف الأول %",
            "R/R الهدف الأول",
            "سبب الهدف الأول",

            "الهدف الثاني",
            "ربح الهدف الثاني %",
            "R/R الهدف الثاني",
            "سبب الهدف الثاني",

            "الهدف الثالث",
            "ربح الهدف الثالث %",
            "R/R الهدف الثالث",
            "سبب الهدف الثالث",

            "الهدف الرابع",
            "ربح الهدف الرابع %",
            "R/R الهدف الرابع",
            "سبب الهدف الرابع",

            "جودة الأهداف",
            "EMA200",

            "ثقة الهدف الأول %",
            "ثقة الهدف الثاني %",
            "ثقة الهدف الثالث %",
            "ثقة الهدف الرابع %",

            "مؤشر RSI",
            "قوة الاتجاه ADX",
            "التذبذب ATR %",
            "السيولة Ratio",
            "Relative Strength %",
            "عدد الأهداف الهيكلية",
            "Backtest Trades",
            "Backtest Win Rate %",
            "Backtest Return %",
            "Backtest Max DD %",
            "Backtest Profit Factor",
            "Backtest Expectancy %",
            "Backtest Avg Win %",
            "Backtest Avg Loss %",
            "Backtest Sharpe",
            "Backtest Sortino",
            "Backtest Calmar",
            "احتمال TP1 التاريخي %",
            "احتمال TP2 التاريخي %",
            "احتمال TP3 التاريخي %",
            "احتمال TP4 التاريخي %",
            "Walk Forward Score %",
            "OOS Return %",
            "Monte Carlo 5% Return %",
            "Monte Carlo Median Return %",
            "Monte Carlo 95% Return %",
            "حالة التحقق",
            "المدة المتوقعة"
        ]

        existing_cols = [
            c for c in preferred_cols
            if c in top_df.columns
        ]

        top_df = top_df[
            existing_cols
        ]

        top_display = top_df.copy()
        if "تاريخ آخر شمعة Close" in df_ok.columns:
            top_display["تاريخ آخر شمعة Close"] = (
                top_df["السهم"].map(
                    df_ok.set_index("السهم")["تاريخ آخر شمعة Close"]
                )
            )

        top_display = top_display.rename(columns={
            "Backtest Trades": "عدد صفقات الباك تست",
            "Backtest Win Rate %": "نسبة الصفقات الرابحة %",
            "Backtest Return %": "عائد الباك تست %",
            "Backtest Max DD %": "أقصى تراجع في الباك تست %",
            "Backtest Profit Factor": "معامل الربح Profit Factor",
            "Backtest Expectancy %": "القيمة المتوقعة لكل صفقة %",
            "Backtest Avg Win %": "متوسط الربح %",
            "Backtest Avg Loss %": "متوسط الخسارة %",
            "Backtest Sharpe": "Sharpe معامل شارب",
            "Backtest Sortino": "Sortino معامل سورتينو",
            "Backtest Calmar": "Calmar معامل كالمار",
            "احتمال TP1 التاريخي %": "احتمال تحقيق الهدف الأول تاريخيًا %",
            "احتمال TP2 التاريخي %": "احتمال تحقيق الهدف الثاني تاريخيًا %",
            "احتمال TP3 التاريخي %": "احتمال تحقيق الهدف الثالث تاريخيًا %",
            "احتمال TP4 التاريخي %": "احتمال تحقيق الهدف الرابع تاريخيًا %",
            "Walk Forward Score %": "درجة Walk-Forward %",
            "OOS Return %": "عائد الاختبار خارج العينة OOS %",
            "Monte Carlo 5% Return %": "أدنى 5% Monte Carlo %",
            "Monte Carlo Median Return %": "الوسيط Monte Carlo %",
            "Monte Carlo 95% Return %": "أعلى 5% Monte Carlo %"
        })
        st.caption(
            "📌 ترتيب الأسهم هنا هو الترتيب التداولي النهائي، وليس التقييم الفني فقط. "
            "عند تفعيل الباك تست يدخل احتمال تحقق TP1 التاريخي والقيمة المتوقعة وR/R وجودة الأهداف وWalk-Forward وOOS ومخاطر التراجع ضمن الترتيب. "
            "لو الباك تست غير كافٍ، النظام يقلل وزنه ولا يخترع نتائج تاريخية."
        )

        st.dataframe(
            display_with_buy_percentage(top_display),
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # الأسهم القوية
        # =================================================

        strong = df_ok[
            df_ok["التقييم"] > 70
        ].copy()

        st.subheader(
            f"🔥 الأسهم القوية: {len(strong)}"
        )

        if not strong.empty:

            strong = strong[
                existing_cols
            ].copy()

            if "تاريخ آخر شمعة Close" in df_ok.columns:
                strong["تاريخ آخر شمعة Close"] = (
                    strong["السهم"].map(
                        df_ok.set_index("السهم")["تاريخ آخر شمعة Close"]
                    )
                )

            st.dataframe(
                display_with_buy_percentage(strong),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "⚠️ لا توجد أسهم قوية حالياً حسب شروط النظام."
            )

        # =================================================
        # جميع الأسهم
        # =================================================

        st.subheader(
            "📋 جميع الأسهم التي تم تحليلها"
        )

        all_display = df_ok[
            existing_cols
        ].copy()

        if "تاريخ آخر شمعة Close" in df_ok.columns:
            all_display["تاريخ آخر شمعة Close"] = df_ok[
                "تاريخ آخر شمعة Close"
            ].values

        st.dataframe(
            display_with_buy_percentage(all_display),
            use_container_width=True,
            hide_index=True
        )

        # =================================================
        # CSV
        # =================================================

        csv_ok = (
            df_ok[
                existing_cols
            ]
            .to_csv(
                index=False
            )
            .encode(
                "utf-8-sig"
            )
        )

        st.download_button(
            "⬇️ تحميل نتائج الأسهم المحللة",
            csv_ok,
            "EGX_AI_PRO_MAX_V8.2_RESULTS_AR.csv",
            "text/csv",
            use_container_width=True
        )

        # =================================================
        # معلومات المحرك
        # =================================================

        with st.expander(
            "🔬 معلومات المحرك المتقدمة"
        ):

            internal_cols = [

                "السهم",

                "_entry_type",
                "_trend_alignment",
                "_data_quality",

                "_ema200_daily",
                "_ema200_weekly",
                "_ema200_monthly",

                "_risk_pct",

                "_rr1",
                "_rr2",
                "_rr3",
                "_rr4",

                "_target_quality",

                "_position_size",
                "_position_value",

                "_pullback_quality",
                "_volume_ratio",
                "_liquidity_ratio",
                "_relative_strength",
                "_structural_target_count",

                "_obv",
                "_obv_ma",

                "_stoch_rsi_k",
                "_stoch_rsi_d",

                "_vwap"
            ]

            available_internal = [
                c for c in internal_cols
                if c in df_ok.columns
            ]

            internal_df = (
                df_ok[
                    available_internal
                ]
                .rename(
                    columns={

                        "_entry_type":
                            "نوع الدخول",

                        "_trend_alignment":
                            "Trend Alignment",

                        "_data_quality":
                            "جودة البيانات",

                        "_ema200_daily":
                            "Daily EMA200",

                        "_ema200_weekly":
                            "Weekly EMA200",

                        "_ema200_monthly":
                            "Monthly EMA200",

                        "_risk_pct":
                            "المخاطرة %",

                        "_rr1":
                            "R/R TP1",

                        "_rr2":
                            "R/R TP2",

                        "_rr3":
                            "R/R TP3",

                        "_rr4":
                            "R/R TP4",

                        "_target_quality":
                            "جودة الأهداف",

                        "_position_size":
                            "حجم المركز",

                        "_position_value":
                            "قيمة المركز",

                        "_pullback_quality":
                            "Pullback Quality",

                        "_volume_ratio":
                            "Volume Ratio",
                        "_liquidity_ratio":
                            "Liquidity Ratio",
                        "_relative_strength":
                            "Relative Strength %",
                        "_structural_target_count":
                            "عدد الأهداف الهيكلية",

                        "_obv":
                            "OBV",

                        "_obv_ma":
                            "OBV MA",

                        "_stoch_rsi_k":
                            "Stoch RSI K",

                        "_stoch_rsi_d":
                            "Stoch RSI D",

                        "_vwap":
                            "VWAP"
                    }
                )
            )

            st.dataframe(
                internal_df,
                use_container_width=True,
                hide_index=True
            )

        # =================================================
        # تفاصيل الأهداف
        # =================================================

        with st.expander(
            "🎯 تفاصيل Target Engine"
        ):

            target_cols = [

                "السهم",

                "سعر الدخول",

                "الهدف الأول",
                "نوع الهدف الأول",
                "سبب الهدف الأول",
                "ربح الهدف الأول %",
                "R/R الهدف الأول",

                "الهدف الثاني",
                "نوع الهدف الثاني",
                "سبب الهدف الثاني",
                "ربح الهدف الثاني %",
                "R/R الهدف الثاني",

                "الهدف الثالث",
                "نوع الهدف الثالث",
                "سبب الهدف الثالث",
                "ربح الهدف الثالث %",
                "R/R الهدف الثالث",

                "الهدف الرابع",
                "نوع الهدف الرابع",
                "سبب الهدف الرابع",
                "ربح الهدف الرابع %",
                "R/R الهدف الرابع",

                "جودة الأهداف"
            ]

            available_target_cols = [
                c for c in target_cols
                if c in df_ok.columns
            ]

            st.dataframe(
                df_ok[
                    available_target_cols
                ],
                use_container_width=True,
                hide_index=True
            )

        # =================================================
        # تفاصيل Entry
        # =================================================

        with st.expander(
            "🎯 تفاصيل Entry Engine"
        ):

            entry_cols = [

                "السهم",
                "التقييم",
                "الإشارة",
                "الاتجاه",
                "نوع الدخول",
                "سبب الدخول",
                "سعر الدخول",
                "وقف الخسارة",
                "جودة الأهداف",
                "R/R الهدف الأول",
                "مؤشر RSI",
                "قوة الاتجاه ADX",
                "التذبذب ATR %",
                "EMA200",
                "احتمال TP1 التاريخي %",
                "قيمة متوقعة %",
                "حالة التحقق"
            ]

            available_entry_cols = [
                c for c in entry_cols
                if c in df_ok.columns
            ]

            st.dataframe(
                df_ok[
                    available_entry_cols
                ],
                use_container_width=True,
                hide_index=True
            )

        # =================================================
        # Data Quality Details
        # =================================================

        with st.expander(
            "📡 تفاصيل جودة البيانات لكل سهم"
        ):

            quality_display = (
                stats_df
                .rename(
                    columns={

                        "symbol":
                            "السهم",

                        "daily_rows":
                            "شموع Daily",

                        "weekly_rows":
                            "شموع Weekly",

                        "monthly_rows":
                            "شموع Monthly",

                        "daily_quality":
                            "جودة Daily %",

                        "weekly_quality":
                            "جودة Weekly %",

                        "monthly_quality":
                            "جودة Monthly %",

                        "data_quality":
                            "جودة البيانات %",

                        "daily_ema200":
                            "Daily EMA200",

                        "weekly_ema200":
                            "Weekly EMA200",

                        "monthly_ema200":
                            "Monthly EMA200"
                    }
                )
            )

            st.dataframe(
                quality_display,
                use_container_width=True,
                hide_index=True
            )

    # =====================================================
    # 🏦 لوحة التحليل المالي والتقييم الاستثماري
    # =====================================================
    if run_financial_scan and not financial_df.empty:
        st.markdown("---")
        st.header("🏦 التحليل المالي الكامل والتقييم الاستثماري")
        st.caption(
            "مصادر التحليل المالي فقط: Yahoo Finance ثم StockAnalysis ثم Mubasher لاستكمال الحقول الناقصة. "
            "لا يتم تغيير مصدر الأسعار أو محرك التحليل الفني. كل حقل يحتفظ بمصدره، والسعر المستخدم هو آخر Close من محرك Daily."
        )
        f1, f2, f3, f4 = st.columns(4)
        f1.metric("عدد الأسهم في القائمة", len(financial_df))
        f2.metric("تحليل مالي متاح", int(financial_df["التقييم المالي"].notna().sum()) if "التقييم المالي" in financial_df else 0)
        f3.metric("متوسط التقييم المالي", f"{financial_df['التقييم المالي'].mean():.1f}/100" if "التقييم المالي" in financial_df and financial_df["التقييم المالي"].notna().any() else "غير متاح")
        f4.metric("تغطية مالية 50%+", int((financial_df["تغطية البيانات %"] >= 50).sum()) if "تغطية البيانات %" in financial_df else 0)

        financial_cols = [
            "الترتيب المالي", "ترتيب داخل القطاع", "السهم", "القطاع", "حالة التصنيف",
            "الحالة المالية", "التقييم المالي", "تغطية البيانات %", "الإيرادات", "نمو الإيرادات %",
            "صافي الربح", "نمو صافي الربح %", "EPS", "EPS طبيعي 3 سنوات", "ROE %", "ROA %",
            "هامش صافي الربح %", "إجمالي الديون", "الدين/حقوق الملكية", "Current Ratio",
            "التدفق النقدي التشغيلي", "Free Cash Flow", "P/E", "P/B", "P/S", "EV/EBITDA",
            "Dividend Yield %", "قيمة DCF", "قيمة EV/EBITDA", "قيمة Residual Income",
            "قيمة Graham", "قيمة مضاعف الأرباح", "مضاعف P/E القطاعي", "مضاعف EV/EBITDA القطاعي",
            "نماذج القطاع", "عدد النماذج المتاحة", "القيمة العادلة", "شراء -10%", "شراء -20%",
            "شراء -30%", "Upside %", "منهج التقييم", "سبب عدم توافر القيمة العادلة",
            "ثقة التقييم %", "تاريخ آخر قائمة", "تاريخ السعر", "مصدر السعر", "المصدر",
            "مصادر الحقول", "رابط StockAnalysis", "رابط Mubasher", "رابط EGX الرسمي", "ملاحظة المصدر"
        ]
        financial_cols = [c for c in financial_cols if c in financial_df.columns]
        fin_top_tab, fin_sector_tab, fin_peer_tab = st.tabs([
            "🏆 أفضل الأسهم ماليًا", "🧭 تصنيف القطاعات", "📊 مقارنة داخل القطاع"
        ])
        with fin_top_tab:
            st.dataframe(financial_df[financial_cols].head(20), use_container_width=True, hide_index=True)
            with st.expander("📋 كل نتائج التحليل المالي للـ201 سهم", expanded=False):
                st.dataframe(financial_df[financial_cols], use_container_width=True, hide_index=True)
                csv_fin = financial_df.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    "⬇️ تحميل التحليل المالي لكل الأسهم CSV",
                    csv_fin,
                    "EGX_AI_PRO_MAX_V10_FINANCIAL_SCAN.csv",
                    "text/csv",
                    use_container_width=True
                )
        with fin_sector_tab:
            sector_summary = (
                financial_df.groupby(["القطاع"], dropna=False)
                .agg(
                    عدد_الأسهم=("السهم", "count"),
                    متوسط_التقييم=("التقييم المالي", "mean"),
                    متوسط_التغطية=("تغطية البيانات %", "mean"),
                    قيم_عادلة_متاحة=("القيمة العادلة", "count")
                ).reset_index()
            )
            sector_summary = sector_summary.rename(columns={
                "القطاع": "القطاع", "عدد_الأسهم": "عدد الأسهم",
                "متوسط_التقييم": "متوسط التقييم المالي", "متوسط_التغطية": "متوسط تغطية البيانات %",
                "قيم_عادلة_متاحة": "عدد القيم العادلة المتاحة"
            }).sort_values("عدد الأسهم", ascending=False)
            st.dataframe(sector_summary, use_container_width=True, hide_index=True)
            classification_cols = [c for c in ["السهم", "القطاع", "حالة التصنيف", "مصدر التصنيف", "قطاع Yahoo", "الصناعة", "نماذج القطاع"] if c in financial_df.columns]
            st.dataframe(financial_df[classification_cols].sort_values(["القطاع", "السهم"]), use_container_width=True, hide_index=True)
            review_df = financial_df[financial_df["حالة التصنيف"] == "معلّق للمراجعة"]
            if not review_df.empty:
                st.warning("الأسهم التالية موقوف عنها إصدار القيمة العادلة القطاعية لحين مراجعة النشاط: " + "، ".join(review_df["السهم"].astype(str).tolist()))
        with fin_peer_tab:
            available_sectors = sorted([x for x in financial_df["القطاع"].dropna().unique() if x != "غير مصنف"])
            if available_sectors:
                selected_sector = st.selectbox("اختار القطاع للمقارنة", available_sectors, key="financial_peer_sector")
                peer_df = financial_df[
                    (financial_df["القطاع"] == selected_sector) &
                    (financial_df["حالة التصنيف"] == "معتمد مبدئيًا")
                ].copy()
                peer_cols = [c for c in ["ترتيب داخل القطاع", "السهم", "التقييم المالي", "تغطية البيانات %", "ROE %", "ROA %", "نمو الإيرادات %", "نمو صافي الربح %", "P/E", "P/B", "EV/EBITDA", "القيمة العادلة", "Upside %", "ثقة التقييم %"] if c in peer_df.columns]
                if not peer_df.empty:
                    peer_df = peer_df.sort_values(["التقييم المالي"], ascending=False, na_position="last")
                    st.dataframe(peer_df[peer_cols], use_container_width=True, hide_index=True)
                else:
                    st.info("لا توجد أسهم مؤكدة التصنيف وذات بيانات مقارنة كافية في القطاع المختار.")
            else:
                st.info("لا توجد قطاعات مصنفة حاليًا.")

        st.subheader("🔬 تحليل مالي تفصيلي لسهم")
        financial_symbols = [x.replace(".CA", "") for x in EGX100]
        selected_financial_symbol = st.selectbox("اختار السهم", financial_symbols, index=0, key="financial_detail_symbol")
        selected_yahoo_symbol = selected_financial_symbol + ".CA"
        selected_row = financial_df[financial_df["السهم"] == selected_financial_symbol]
        selected_metrics = selected_row.iloc[0].to_dict() if not selected_row.empty else {}
        snap = get_financial_snapshot(selected_yahoo_symbol)
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("التقييم المالي", f"{selected_metrics.get('التقييم المالي', np.nan):.1f}/100" if pd.notna(selected_metrics.get("التقييم المالي", np.nan)) else "غير متاح")
        d2.metric("ROE", f"{selected_metrics.get('ROE %', np.nan):.1f}%" if pd.notna(selected_metrics.get("ROE %", np.nan)) else "غير متاح")
        d3.metric("ROA", f"{selected_metrics.get('ROA %', np.nan):.1f}%" if pd.notna(selected_metrics.get("ROA %", np.nan)) else "غير متاح")
        d4.metric("هامش صافي الربح", f"{selected_metrics.get('هامش صافي الربح %', np.nan):.1f}%" if pd.notna(selected_metrics.get("هامش صافي الربح %", np.nan)) else "غير متاح")
        st.write(
            f"**الحالة:** {selected_metrics.get('الحالة المالية', 'غير متاح')}  |  "
            f"**القطاع:** {selected_metrics.get('القطاع', 'غير متاح')}  |  "
            f"**حالة التصنيف:** {selected_metrics.get('حالة التصنيف', 'غير متاح')}  |  "
            f"**الصناعة:** {selected_metrics.get('الصناعة', 'غير متاح')}"
        )
        if selected_metrics.get("سبب عدم توافر القيمة العادلة"):
            st.caption(f"سبب عدم ظهور القيمة العادلة: {selected_metrics.get('سبب عدم توافر القيمة العادلة')}")
        st.write(
            f"**القيمة العادلة:** {selected_metrics.get('القيمة العادلة', np.nan):,.2f}  |  "
            f"**شراء -10%:** {selected_metrics.get('شراء -10%', np.nan):,.2f}  |  "
            f"**شراء -20%:** {selected_metrics.get('شراء -20%', np.nan):,.2f}  |  "
            f"**شراء -30%:** {selected_metrics.get('شراء -30%', np.nan):,.2f}"
            if pd.notna(selected_metrics.get("القيمة العادلة", np.nan)) else "القيمة العادلة غير متاحة لعدم اكتمال مدخلات التقييم."
        )
        if snap.get("error"):
            st.warning(snap["error"])
        st.caption(f"المصدر: {snap.get('source', 'Yahoo Finance عبر yfinance')} | آخر قائمة دخل: {_financial_period(snap.get('income'))} | آخر ميزانية: {_financial_period(snap.get('balance'))} | آخر تدفقات نقدية: {_financial_period(snap.get('cashflow'))}")
        tab_income, tab_balance, tab_cash = st.tabs(["📈 قائمة الدخل السنوية", "🏛️ الميزانية العمومية", "💵 التدفقات النقدية"])
        with tab_income:
            if isinstance(snap.get("income"), pd.DataFrame) and not snap["income"].empty:
                st.dataframe(snap["income"].T, use_container_width=True)
            else:
                st.info("قائمة الدخل السنوية غير متاحة لهذا السهم من المصدر الحالي.")
        with tab_balance:
            if isinstance(snap.get("balance"), pd.DataFrame) and not snap["balance"].empty:
                st.dataframe(snap["balance"].T, use_container_width=True)
            else:
                st.info("الميزانية العمومية غير متاحة لهذا السهم من المصدر الحالي.")
        with tab_cash:
            if isinstance(snap.get("cashflow"), pd.DataFrame) and not snap["cashflow"].empty:
                st.dataframe(snap["cashflow"].T, use_container_width=True)
            else:
                st.info("قائمة التدفقات النقدية غير متاحة لهذا السهم من المصدر الحالي.")
        st.info(
            "منهجية التقييم القطاعي: لكل قطاع مؤشرات مالية وأوزان ومضاعفات P/E وEV/EBITDA خاصة به. "
            "القيمة العادلة هي وسيط النماذج المسموح بها للقطاع فقط. الأسهم المعلقة للمراجعة لا يصدر لها سعر عادل قطاعي. "
            "مضاعفات القطاعات افتراضات أولية معلنة وليست متوسطات سوقية مستخرجة آليًا؛ يجب معايرتها لاحقًا ببيانات الشركات النظيرة والإفصاحات الرسمية."
        )
        with st.expander("🧮 معادلات تقدير السعر العادل المستخدمة", expanded=False):
            st.markdown(
                "- **DCF:** القيمة الحالية لتدفقات FCF المتوقعة 5 سنوات + القيمة النهائية، ويُستخدم فقط في القطاعات التشغيلية عند توافر التدفقات.\n"
                "- **EV/EBITDA:** (EBITDA × مضاعف القطاع − الديون + النقد) ÷ عدد الأسهم.\n"
                "- **Residual Income:** القيمة الدفترية للسهم + القيمة الحالية للدخل المتبقي المتوقع (ROE − تكلفة حقوق الملكية)، ويُستخدم خصوصًا للبنوك والماليات والعقارات.\n"
                "- **P/E القطاعي:** وسيط EPS لآخر 3 سنوات × مضاعف الربحية الافتراضي للقطاع، مع معامل تعديل عام من الإعدادات.\n"
                "- **Graham:** يُعرض كمؤشر مرجعي فقط ولا يدخل في القيمة العادلة القطاعية النهائية.\n"
                "- **التجميع:** وسيط النماذج المتاحة والمسموح بها للقطاع؛ مضاعفات القطاعات أولية وتحتاج معايرة بمقارنات السوق."
            )

    # =====================================================
    # الأسهم الفاشلة
    # =====================================================

    df_failed = df_all[
        df_all["الحالة"] !=
        "✅ تم التحليل"
    ].copy()

    if not df_failed.empty:

        st.subheader(
            f"⚠️ الأسهم التي فشل تحميل/تحليل بياناتها: {len(df_failed)}"
        )

        st.dataframe(
            df_failed[
                [
                    "السهم",
                    "الحالة"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        csv_failed = (
            df_failed[
                [
                    "السهم",
                    "الحالة"
                ]
            ]
            .to_csv(
                index=False
            )
            .encode(
                "utf-8-sig"
            )
        )

        st.download_button(
            "⬇️ تحميل قائمة الأخطاء",
            csv_failed,
            "EGX_AI_PRO_MAX_V8_2_ERRORS_AR.csv",
            "text/csv",
            use_container_width=True
        )

    # =====================================================
    # 🧭 مستشار قرارات المحفظة — نظامان مستقلان
    # =====================================================
    st.markdown("---")
    st.header("🧭 مستشار قرارات المحفظة")
    st.caption(
        "قرارات التداول تعتمد على إشارات ومستويات المحرك الفني، وقرارات الاستثمار تعتمد على التقييم المالي القطاعي. "
        "لا يوجد دمج بين المحركين ولا درجة فرصة موحدة، ولا ينفذ البرنامج أوامر بيع وشراء تلقائيًا."
    )

    def _advisor_symbol(value):
        return str(value).upper().strip().replace(".CA", "")

    def _advisor_latest_close(market_data, symbol):
        """استخراج آخر Close من نفس بيانات Daily التي استخدمها الفحص الفني."""
        try:
            if isinstance(market_data.columns, pd.MultiIndex):
                first = market_data.columns.get_level_values(0)
                second = market_data.columns.get_level_values(1)
                if symbol in first:
                    part = market_data[symbol]
                elif symbol in second:
                    part = market_data.xs(symbol, axis=1, level=1)
                else:
                    return np.nan, ""
            else:
                return np.nan, ""
            if "Close" not in part.columns:
                return np.nan, ""
            close_series = pd.to_numeric(part["Close"], errors="coerce").dropna()
            if close_series.empty:
                return np.nan, ""
            stamp = close_series.index[-1]
            try:
                stamp = pd.Timestamp(stamp).strftime("%Y-%m-%d")
            except Exception:
                stamp = str(stamp)
            return float(close_series.iloc[-1]), stamp
        except Exception:
            return np.nan, ""

    portfolio_holdings_for_advisor = portfolio_result.get("holdings", pd.DataFrame()).copy()
    if portfolio_holdings_for_advisor.empty:
        st.info("سجّل عملية شراء واحدة على الأقل، ثم شغّل فحص الأسهم لعرض قرارات مراكزك.")
    else:
        tech_lookup = {}
        if isinstance(df_ok, pd.DataFrame) and not df_ok.empty and "السهم" in df_ok.columns:
            tech_lookup = {
                _advisor_symbol(row.get("السهم")): row
                for _, row in df_ok.iterrows()
            }
        fin_lookup = {}
        if isinstance(financial_df, pd.DataFrame) and not financial_df.empty and "السهم" in financial_df.columns:
            fin_lookup = {
                _advisor_symbol(row.get("السهم")): row
                for _, row in financial_df.iterrows()
            }
        manual_price_map = {}
        cleaned_manual_prices = _portfolio_clean_prices(st.session_state.portfolio_prices)
        if not cleaned_manual_prices.empty:
            manual_price_map = dict(zip(cleaned_manual_prices["السهم"], cleaned_manual_prices["السعر الحالي"]))

        trade_advice_rows = []
        invest_advice_rows = []
        for _, holding in portfolio_holdings_for_advisor.iterrows():
            symbol_full = str(holding.get("السهم", "")).upper().strip()
            symbol = _advisor_symbol(symbol_full)
            market_price, market_date = _advisor_latest_close(daily, symbol_full)
            price_source = "آخر Close من Daily"
            if not np.isfinite(market_price) or market_price <= 0:
                manual_price = manual_price_map.get(symbol_full, np.nan)
                if pd.notna(manual_price) and float(manual_price) > 0:
                    market_price = float(manual_price)
                    market_date = "يدوي"
                    price_source = "السعر اليدوي المدخل بالمحفظة"
            qty = float(holding.get("الكمية الحالية", 0) or 0)
            avg_cost = float(holding.get("متوسط التكلفة", 0) or 0)
            pnl_pct = ((market_price / avg_cost) - 1) * 100 if np.isfinite(market_price) and avg_cost > 0 else np.nan
            tech = tech_lookup.get(symbol, {})
            fin = fin_lookup.get(symbol, {})

            if str(holding.get("التصنيف", "")) == "تداول":
                action = "بيانات غير كافية"
                reason = "شغّل الفحص الفني وتأكد من حداثة آخر Close ومستويات السهم."
                entry = tech.get("سعر الدخول", np.nan)
                stop = tech.get("وقف الخسارة", np.nan)
                target = tech.get("الهدف الأول", np.nan)
                signal = str(tech.get("الإشارة", "غير متاح"))
                entry_type = str(tech.get("نوع الدخول", "غير متاح"))
                score = tech.get("التقييم", np.nan)
                if np.isfinite(market_price) and market_price > 0 and tech:
                    if pd.notna(stop) and float(stop) > 0 and market_price <= float(stop):
                        action = "خروج / بيع"
                        reason = "السعر وصل إلى وقف الخسارة أو كسره وفق مستوى المحرك الفني."
                    elif pd.notna(target) and float(target) > 0 and market_price >= float(target):
                        action = "بيع جزئي / جني أرباح"
                        reason = "السعر وصل إلى الهدف الأول؛ راجع جني جزء من المركز وتحريك الوقف وفق خطتك."
                    elif entry_type != "انتظار تأكيد" and any(x in signal for x in ["قوي", "🔥", "🟢"]) and pd.notna(entry) and float(entry) > 0:
                        if market_price <= float(entry) * 1.02:
                            action = "شراء / زيادة تدريجية"
                            reason = "الإشارة الفنية قوية والسعر قريب من نطاق الدخول المقترح."
                        else:
                            action = "احتفاظ / لا تطارد السعر"
                            reason = "الإشارة إيجابية لكن السعر ابتعد عن مستوى الدخول؛ انتظر إعادة اختبار أو فرصة جديدة."
                    else:
                        action = "احتفاظ / انتظار تأكيد"
                        reason = "لا توجد حاليًا إشارة دخول قوية مكتملة أو إشارة خروج مؤكدة للمركز."
                trade_advice_rows.append({
                    "السهم": symbol_full, "الكمية": qty, "متوسط الشراء": avg_cost,
                    "آخر سعر": market_price, "ربح/خسارة %": pnl_pct,
                    "الإشارة الفنية": signal, "نوع الدخول": entry_type,
                    "سعر الدخول": entry, "وقف الخسارة": stop, "الهدف الأول": target,
                    "قرار البرنامج": action, "سبب القرار": reason,
                    "تاريخ السعر": market_date, "مصدر السعر": price_source
                })
            else:
                action = "بيانات مالية غير كافية"
                reason = "شغّل التحليل المالي وتأكد من تغطية البيانات والقيمة العادلة قبل اتخاذ قرار استثماري."
                fair = fin.get("القيمة العادلة", np.nan)
                buy10 = fin.get("شراء -10%", np.nan)
                buy20 = fin.get("شراء -20%", np.nan)
                fin_score = fin.get("التقييم المالي", np.nan)
                coverage = fin.get("تغطية البيانات %", np.nan)
                confidence = fin.get("ثقة التقييم %", np.nan)
                fin_status = str(fin.get("الحالة المالية", "غير متاح"))
                sector = str(fin.get("القطاع", "غير متاح"))
                if np.isfinite(market_price) and market_price > 0 and fin:
                    reliable = (pd.notna(fin_score) and float(fin_score) >= 60 and
                                pd.notna(coverage) and float(coverage) >= 50 and
                                pd.notna(fair) and float(fair) > 0)
                    if pd.notna(fin_score) and float(fin_score) < 45:
                        action = "مراجعة تخفيض المركز"
                        reason = "التقييم المالي ضعيف؛ راجع أسباب الضعف والنتائج والإفصاحات قبل الاستمرار."
                    elif reliable and pd.notna(buy20) and float(buy20) > 0 and market_price <= float(buy20):
                        action = "زيادة استثمار تدريجية"
                        reason = "السعر عند أو أقل من مستوى القيمة العادلة بخصم 20% مع تقييم مالي وتغطية بيانات مقبولين."
                    elif reliable and pd.notna(buy10) and float(buy10) > 0 and market_price <= float(buy10):
                        action = "شراء / زيادة تدريجية"
                        reason = "السعر داخل نطاق خصم 10% من القيمة العادلة؛ الزيادة تكون على دفعات."
                    elif reliable and market_price >= float(fair) * 1.15 and float(fin_score) < 70:
                        action = "مراجعة جني أرباح"
                        reason = "السعر أعلى من القيمة العادلة بأكثر من 15% مع تقييم مالي دون 70؛ راجع وزن المركز."
                    elif reliable:
                        action = "احتفاظ"
                        reason = "لا يوجد حاليًا هامش أمان كافٍ للزيادة ولا إشارة مالية قوية تستدعي الخروج."
                    else:
                        action = "احتفاظ / إيقاف الزيادة"
                        reason = "التغطية أو الثقة أو التقييم لا تكفي لإصدار قرار زيادة استثمارية موثوق."
                invest_advice_rows.append({
                    "السهم": symbol_full, "القطاع": sector, "الكمية": qty,
                    "متوسط الشراء": avg_cost, "آخر سعر": market_price,
                    "ربح/خسارة %": pnl_pct, "التقييم المالي": fin_score,
                    "تغطية البيانات %": coverage, "ثقة التقييم %": confidence,
                    "القيمة العادلة": fair, "شراء -10%": buy10, "شراء -20%": buy20,
                    "قرار البرنامج": action, "سبب القرار": reason,
                    "الحالة المالية": fin_status, "تاريخ السعر": market_date,
                    "مصدر السعر": price_source
                })

        trade_tab, invest_tab = st.tabs(["⚡ مستشار التداول", "🏦 مستشار الاستثمار"])
        with trade_tab:
            st.caption("قرارات قصيرة/متوسطة الأجل. مستويات الدخول والوقف والهدف مأخوذة من المحرك الفني، وليست أسعار تنفيذ مضمونة.")
            trade_advice_df = pd.DataFrame(trade_advice_rows)
            if trade_advice_df.empty:
                st.info("لا توجد مراكز تداول مسجلة حاليًا.")
            else:
                st.dataframe(trade_advice_df, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ تنزيل قرارات التداول CSV",
                    trade_advice_df.to_csv(index=False).encode("utf-8-sig"),
                    "EGX_Portfolio_Trading_Advice.csv", "text/csv",
                    key="portfolio_trade_advice_csv"
                )
        with invest_tab:
            st.caption("قرارات شهرية/طويلة الأجل. الزيادة مشروطة بوجود قيمة عادلة قطاعية وتغطية بيانات كافية؛ لا يتم استخدام المؤشرات الفنية كبديل للتحليل المالي.")
            invest_advice_df = pd.DataFrame(invest_advice_rows)
            if invest_advice_df.empty:
                st.info("لا توجد مراكز استثمار طويلة الأجل مسجلة حاليًا.")
            else:
                st.dataframe(invest_advice_df, use_container_width=True, hide_index=True)
                st.download_button(
                    "⬇️ تنزيل قرارات الاستثمار CSV",
                    invest_advice_df.to_csv(index=False).encode("utf-8-sig"),
                    "EGX_Portfolio_Investment_Advice.csv", "text/csv",
                    key="portfolio_invest_advice_csv"
                )

    # =====================================================
    # الحالة النهائية
    # =====================================================

    st.success(
        f"""
🔥 الفحص اكتمل بنجاح

📊 إجمالي الأسهم: {total}

✅ تم تحليل: {analyzed}

❌ فشل: {failed}

📡 نسبة تغطية البيانات: {coverage:.1f}%

⭐ متوسط جودة البيانات: {avg_quality:.1f}%

📅 Daily Coverage: {daily_coverage:.1f}%

📆 Weekly Coverage: {weekly_coverage:.1f}%

🗓️ Monthly Coverage: {monthly_coverage:.1f}%

📐 Daily EMA200 الحقيقي: {daily_ema200_coverage:.1f}%

📐 Weekly EMA200 الحقيقي: {weekly_ema200_coverage:.1f}%

📐 Monthly EMA200 الحقيقي: {monthly_ema200_coverage:.1f}%
"""
    )
