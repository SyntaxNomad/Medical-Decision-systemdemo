# ui_components.py - Clean UI components separated from logic

import streamlit as st
import time
from datetime import datetime
from config import APP_TITLE, APP_SUBTITLE, EXAMPLE_CASES, COLORS
from utils import get_validation_feedback

def render_header():
    """Render the main header with logo"""
    st.markdown(f"""
    <div class="header-with-logo">
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACbCAYAAACAn2I8AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyRpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDcuMC1jMDAwIDc5LmRhYmFjYmIsIDIwMjEvMDQvMTQtMDA6Mzk6NDQgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjdDMDU2REZFMTE3NzExRUM4MjM5OThCRTQ4MTJBQTEzIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjdDMDU2REZEMTE3NzExRUM4MjM5OThCRTQ4MTJBQTEzIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCAyMi40IChXaW5kb3dzKSI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjE5MjBFOEUyMEZCNjExRUM5NTI5QTg0OURDMjM0Q0Q3IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjE5MjBFOEUzMEZCNjExRUM5NTI5QTg0OURDMjM0Q0Q3Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+RYnPgwAAHUxJREFUeNrsXQeYFUW2PkPGAckmQIJEAwgIiBhxdQ2rmFcFFWV5JnimXdNbFePqrijmiKKsiXVBxYySlSgSJAdRQMlBsgxzX/323980bVff6nDvhNvn+8430LdCd/XpUydXXiqVEgeUU9hD4aUKj1e4D68vU/iewhEKpyrcIgkk4AN5DsJqqPB5hacqrKBpv0PhYoWTFY5ROEXhEoWFyVIm4EVYdUgohwfsv1PhHIUTFH6p8BuFPyXLmoBNWP0V3hPDeOsVfqtwrMJxCmcq3Jwsc24SVlX19yuF7TIw/g+UyUaRqy1Q+Guy7LlBWE348utkeK4ChfNJYKMpny1LXkHZJax23LaqZXluaJazuW1CvpuucF3ySsoOYZ2k/n6ksGox38vPJK7RJLa5Crcnr6j0EtaJ6u/HJYCw3LBQLLMG5LOvxTJzJGaNhLBiBdusMY7cDDJhYtZICCt2gFljhkM+myWJWSMhrAxAYtYoYVChjDxHI+IFCvdQ8P9KitxO3yevOuFYccNWsTwA4yQxaySElUFwmjUmUttcT06XQEJYscAGhf9W+CK1zgQSGSsSYGt8RizD8CpJ7GMJYUUExJPdpfCpgFpjNYe8lkBCWHvBcoUXi2XFDwqIrD1GYXuOg9izxECbZsFyRWA/MyRRAX5R+KlYodkXUeAfr/AfCk9XuF9CSrknvO/my/8yxjEfU3iT4/92gONEEhz+ndMmjVzYCp+OmagANytM8S8AsWx/IAJWk7jgBYChdjaJL+FYJRSgvdn2pooG7dcoPCxD3CNPrMylsw3arhTLdjae2/Fsbq8JxyomKOCL+IwmglXc2vBSaymsr/AohZ3FCq2u4ur/Rga3JHCsqxV24H34QX3iWQ5FYgoJbZLC7xRuSzhW5gFc6TVuY98a9mlBWerPCrvwWhe+uExCT4VDIo7xg0M+w4e0gKaRhLBiBAT4XStWpEJYOEXhOWLZrDZkeg1JEF1j5IRLKJtBRkOw4zIpZUnCJY2w4Ci+mOaB0gRniGXFz9SW+z239YellIRrlyQ71mRymdJGVADYuL7JIEdsSu77gRSVPUgIywB+pmy0sZSKFNBWB2VhnpNJYAlhGcJ1FGBLMwyX7IRHX2+ghSaEpeAdsexBpR1gChmThXmqK/xTQlj+ANvNPVJ24P0szdM1ISx/GCqWzaasAEwEu7IwT7OEsPQAI+izUrZgqcJFWZinrpi5tHKSsKZmUEUvLoAL6rsszFNJfu++SgiLAIE9JWUP3hLLyZxJSJX0tStOwvoyS/PAwFg5i88FIyYc4seKZdvaKTkIcUc3wN2wSayIAhg7d5B4U/xbU6yoBPi95mXh+RBOPIAqOiIkXpHsZOPsoSAPfFzhfQrPyyXCiuorXEg56WsSymIHQe3WcMgq/JvpxAQIuIiBaui4toNb1eNZkoWc0E/ho5SPosIyhUdICU7uCMOxUJUPVuYPxSrMEcQpWijZc6Ke6yIq4cdzlVjlxt9UODAL8pANyAxaznnLfA5nEBnrC4UXihXYdie5VEn2tB/p81sVEhhitZ4Uy8mbLYXlmlzYCk0IC4uPADrEOL0rpafKngmx7MMtCs94apbu63USc84SFgRsJAscJ1ZYSGlTSoJwoXoKX6ZykQ34O+XRnCOsqSQoCLkFpfC54P0/IGAfyGNdsnR/+GgfyDXCgv8OcT8zi/G+Giu8Qawk03IhCWvfEP0ODnm/rXm/3QL0GVqWuZb90vL492lqTMUZX32gWMbTgdQ8EVnaR4JFTiJwMIwzeFOIPs3FKlk5kPeN+HdkS6fz5e0gcZVZwrJtS69RkC3uOlFXuOQjpHe9SAEbmpyJHQgx4n+TYLl72PIXhrjf6ymj2QCLO2LMYBw9x/HRegHCbFJllbAg6MJAenUJNxPAIAgXCTJXLjAY5ymaRp405MDwFiwJcb8dNNc7imXvG03RwgtgpP2hrBIW8vb+ItmJI4rDTIAX9h+FDxqMtZiyj01gm9O0DZqdDENngzRtThDLBniTx2/bQ3LJUkFYayVcZgy2pBspk8VlSa5p8KJsgJG2vWHbRSSwTpQjvQhsfoj7Pci1DfoBPoRGHtdnSylPTg1ibjCVhWCOQL4bsnh7SXQ/WNOAZoKg5oGFlCNtAtviENpfDXG/LRXmB+BuR3lcv1es+hI4KxJFRfpyy19SmgkrSnTDsY5/t+WLuY4vbnLIMXekEXbdELbegU1gT1B2mxNySwrKabycxlscBD5HisKJQLAnUTk4LZc4VguN/DMowtY4n1uGqVF2VsTnX0wBO6ycM4EaqylRzQv40cDcAnfahVLKEnnDElae6N0fdSR82CxUb7g7kIWC8JbdPm1RoujHYl6/3dSmcTB7uohY3OuqkPO8yzlmlnXCskv4jNZwgU0R72sKlQLbJuTFwRCCsqGErCOMoudy6/pAQ2CQmaIcw4J1PYcfVJWySlgAFPCACwOFx8a6trO4jH4gMBQJOYYEVujahjJVRvtEsaz9l1JANwWsQ3f2/8BjvaLCMsqGqYCyaNbBPmw8DgCBIUP3mQyybGhzV1L+QGHZuMsvwhH9ksI/Oq4hZh1W/7dJLEFkHdiwepK7/ismswII6nmxEn1X5QJhlXbIp0bW2afNOhLXq+SYxQVHc2tdmxBWyYfbyQWDaITgbvD3ZfusxDxiYUJYJRuQxQMLeKOQcg+iQnEmz6JkKRPCcgIMkJ9EHANy33DKP1/FeG/QNM/ntjdMspf8kRBWDABBuH9MY2FBR4pVlwJRI7sjjAXzAmxY5fl/BArgdIyBMRNviTI3lCWoG7P8g8SM96hN9gq5zoiAfcxBVABkdCNkCHazD2nWSAirBEO9DI3bnhrkRyGIF5pfEx/iRdg2DNQIIeqSEFY0gNMceXnwz/2vWGErJZmwnDLcUAlWQ6K1YTubg6HW/BEJYYUDyBbPiWUVR2TCTP5tEXHrqpOFe4cQ3jdA+yDF1bBdwhCL8KXrEuE9+NYwUfMb7Ej2SRZBVX5EYqCqYMMsPAMs8Ii9MgmV/kTCh8vA4j+uOF9WNjkWuMoBEfpf6PNbDW6N08jBGgcYF32zVTsdxHucIQeKkvbfL1e2QiQTILYeRUT+GfDF29DKUJMCgaHKzIOGshPCf/KzuOadDdo0jig/HunSJsssYZ1HrrC/WGlZ4Cz9yS1MhfYgyaSowYWYeESypqswHCV+LAyYcCJ4AqpFmKNyrhBWM4+XCaPkS4YLAEJpEGJeqOtvp1H1W2V5zU0ytJEStiLCHIiHK8gFwmruoymZcK1GEi5lXkiQ50V80XGCSZrdRspJYc9aROx8YS4QFhy0XtGTKw01pMMj3utRPr/Nz/KarzRsB8s9apnixK/1IQgrJ4T3u8UK0nvdRWAwDZj40qKeEu/HFb+S7GYjLw/QFtvhHWJZ8EFgpvFXs3OFsAAwZiIX8WgSGJIL/mvYN6rD1U9eQfbzbVlch+9D9PmRBIYsqEfSEFjYGhTxAgykxYQ1A7Z/QOHOVDjoZTB+b4XLU5mHzjGs3cEKH1a43mP87xXmF+N7/Q2L06UTNJMHaWFwtg6R4KEoJnLUIMo0yD6amKFn3ibxxOmDg91Oe5WTg22m2FHsB5eX1ngsLCiKbCCDJ11aPzSsFiE0LGisvcXKuqkW031DcD9M4g9lbkAFBzJriUjNL+2BfhBqUewDp7PqIgemUzYJq34j/auHWE7eJhHvF0J1G8kBKO3xWNOpEHT1MWl8G9Gms4DbSzsSF2Kgwn6NKyVHoKwE+uF0jMuocYLAbCMkaiU8GtMc2L5QWacbCfmVEHLiwlwhrLIa8w55A7VMJ0vwYmpBoJFjmzQJzIPcNiYhrARMAU5sVIVBZUTEu3uVh0K8WK+EY+UuIAoDlvqwZYNQlvJysdL061H1f4dy2o6EsHITIKDjECXUiccxdAiDHhVyLJhBapOwtuTaQiaEtbci8wXlICcgRxBpWJ8mS5QQVhgAl4JxUWcPQ/IpHMHjk6XKHXNDHNBY/NOzzhCr/tVzkt2jgBPCKuVgEjKMVLFrKIgnkBCWERwWoO0lkv6snISwEvgNgmTFFHuyQkJYpQc+DNB2mZScI2JMoXxCWMUDqK1wlqHWh8OV4lCnEY5zn1gxYDUy9FxQSpBVjcNNEdPWMCurWdyRhiUQYYLprnCsTxRov5jm+qtjzIUK+yqsFvOzjHDdO6JO/6GwQSbXMSEkPZZTeK7C8R6EdUJMcwz1GPs7hcfHNH4ThTs0H8daEtiBZS00uaQDYrhQ+hG1Fs7jFrmNW+bkmGSelhrt9KmYbGXIHtdleSOJ93ZukbHXenASFsJ3ESGJGkvVffpUYdtMCoNNKX/kcfHDpMDni3laPto2F31RfhAYjhxBRjeiVXfGRFg64tk3JnPGIQZt4HHAWY5XZIqwBit8QawIyZN8+iA05APJ3MkIINpvKGSeKFY5njDZyjjy7gnDtqjzMMRAII+zYD+iXXuJVe3PDXAtbY1hjiCF2PrGySyccUMX8GGrU53WQU1ykEylcFflHAW8l/yQc+0v5sfm1SkmgydqlOI0D0Sl3iKW2wgwK6bxmwdoW49rvzVOwkJ4R0+yTrB5HAQ0wMHyMSnqUw0i8bkPJO/M3/ejavuW4VawhxwKhcJe4f8LpaigRaGEP/y8wMWRsb2ezIVD0f/trrZu4kVbHLy0D9u/n0ECG0XEnIjjeimmcSEXnmnYdoXEmDZWji94MAU5bAXtuDU45RqcwvUM27pfwE388k4RKw0J8UyPOH7HlnmUQ95pwQduzP+DoPtLZotYHEaB+36xis2+lYbt49wbhNB0pIyHOgo3Z4GD4ciVWyW+gwgG8r2apPXPlvgO1/qNsJqRKHD40TW8GbdVeQ+/8JTGWIhFb0uWfifZ+oEOQfQLCr/C68c6uMluyXyC5V/FSnwA1zqb6JeGhXIAfciJkTjxLI2L2ar8Fxfs4keONLk70hBYrAdrlSMnwctdwGuVSUCFLsLay67qILKRFJSdFuxyjhdXjlyrwDHWbp+vo8DB6eIwGQAQLvw5P45v+be+q53zeZHp87Lj/8jOqRVQZilJgGTdh7lzgMC8DhCdFzdhraTgam9NTTzMDdXYppBbSAUfwljOF2dXIt5EYrK5kh2ma2fP7OC4KYc8V0HMD43cnxzQixDta5j7IMe/C2Xv7J0aoj8xFrCQ93eAlG5Y4yCw/5OiYilfUxOPDSpwP58iRSdZ9SQRDePXDcCBkBPIWkGIjdh+k8YmlE+zRDtqGvjar+N2eDDHx0lbG3itEeUaoRIwm19VJ24/ftyrN7fwxi5idx4WieC81yhfbSFXvlEs32BNPjM+MlS/WeoxRy2OVVaSIVDr4SGx6uU353pvjXMCOzS5KQXb1lzcmbRrNCC3gS3pAYWrSSj3U4Px4lz4/2a2q+z4PwikEre6rZS9ylHz/NVhq4KqfQ9tObBjocTQxaKvdwAzyTvkSKsd14dzfluFv0qspNb6XMyF/FB2cfteRSKt66FIFHL+a+LeMsoqmMa815aSc/6yl11tKc0ct5CLtqH6/iIVi6bkgCBqVG3+H3K4TQkJZAZMfIWN+FJOKKHPsInbLFwty8TKB5xMjjeAbTqRI/1ADfHmhKiKn2NhC4MT9jMpwUfFOswmVajhjnUoDNiyu5NzQVacmLz6krEVJpBAYK0wgQSiQAOaYTaKo+hbUMKCLxGlgo6gFlaDchpsQijaOok2kaCCfh41xpTrGrSx3RlaEDxLFz5LfWqlKWqWSx22nahegYoe5pI8asKpDI9T2WCOPAkXvw+CwrEy1WiCqs93eK/CaSaElU/B+HIKwVXTtIfRDf7Cp8T8dIV+VOVTLsXiLrGOro0LKvJZepGo0rloFvNZnpNwITPNaPYo73i2PJo6LhDz0yMgGw5zfXx5VFbOE+/4MLjWehoS1jY+6xTKptPT9DmIzzWU7WE+WkTTjlVVJ02I6SUK54WsDvyzwh6Goayfa8Y4OsZw2TMVfhPyWZZzLYLOeZFmvPcCjnOJZpwRPn0mhHzWPQpHM+5fN/arCm9gWPMmxuuPVFhe4el4n7qOtRQOian89C1pFq2GwhUawqwRU+z6v2J6lrsDzv2gZpybAo7zWMBx8P5Wx/C8byis5xq7Dom2ksIjFS5V2ErhFoUns80XXnYs+N4+JRtNByaxUijV2CeNrHOgx3W4GaJWF4bp4W3aruJ4lnu5xZhCO8316QGfo6PHtZToY+8PleineQDgyhspex8DCNlqi0O2wzzvU76ewTYrK3hYsUdoHkQoTI/k/grXy3YKiEdSdumm6YeQZ/gdp3n81kFjqJ0ag/EXgYl+B2h+xkWZyWcBIbZhnz9o+jzIZ/nEwP53mMagG8QttJ9mHCgZczV9Omiur6FilecgzsqUmXTx920p557MDx22zOpc30LKZ/DMIFzdrmFf152DNsyHLX5pcKrCVZrTI8aSbXr1GaSZr3vELfBWn2eZrrBbmv4XKFyj6T/fIP+vrcLdHn2/Dvgc3TT38KlPn39r+pzJLayyA6sqPFThnQp/8lmzZx10AhnxUqaXQb46ibLWaXzP450308dn0BcUVjBciIsd/eZR8MzzkX++9ZhvO286LFG19cmnGxbguJVjeS9e8Jc0fXukeUGmeJtmnHs07UE4cz3ab1a4f5q5GvkI/b8qbMd2hzP/8XKFXR3XIPPNUHiGPWA9Css6AS4v4GI8qfA+hfumaddY4VaPOWdTwwhLWO9rnmUCv9A4BPAxadZloKbflQHn1+0ip2raN9d8VJP5IaebD8S3RDPn8452HRR+rHAwlaPn+f+znJnQf9MMtMCAOKLgnzTzvh5hzI5Umb2+2FYhxmvIvm7YliZNfYxHnwIfkcALq1LrcsMGhQdo+pwfA6e8QjPGDx4iQCdmjIO7V3RmQu9D6d8L7pLM1knvork+JcKYvTXKAEJowhx6uVyjSGDdDtf0gRLkVff9Zwl21g0MrF5Jt3N9DLa6w8wnBZh3OAV9L2t7S493NZzO/d1OzekEjdYBzeW9DPuZOmjU6LCEBS/BaR7X4bJ4OcJ96vL8dJVbQFT1PK7PkWAVlNuLdzbRpICmiT0SLFniF80zlxPDajVoeLZ4J2sOF/O48zBQTbwzdVdJ+KNB8IE08rgOn9+CCPe62mf9vKCNeIdTBzWh6Di6LuynFm1YXm62oGuqO/entilhdQ1483FBa41hdK6ED8LTpZRHPaFVR0CpgAQxLeCcXhx9p+gTH3ScEna3oPH6Oqay2/TmW3lcLxDvpII4ob3mq45SyUV37FvUOHVdGUmvQy3Lawh8hwRLnT9IvKvRzBd9fmBHzZqGycDRZSStMiWsihpqzXSMeyfN9SgW93zN9Y0R7/VwDbdaqnkhXvmHS8U82sOes7qGSPYEXNOgMmsljfLxqxgejadj8RUks1m/FcixvNj8rAzNFxbqa3x+P4l3KryuDNQsCRZbptPuxmmuV6T7xcuF9F0IpeoQjay2xJSwtmkoNpO1KvGyWnhcXyRmdQZ0oAtYOzjCmFBuvOqDIhDQKxevZQzylY6wCny2tYY0T3itadADp/pqttTRYhgUCMKaofmtawYJ6wgNR5wh0SJGFwX8+k22hOs1vw3VXNcFQgZRSBDNeqTH9WViBeTpNNHKmq0zSKQqEogv0vz2ZhDN43PNb38OuYUcY9BGFz0RtQQj5DOvqjXwzIcJI7lVvG18CMP+WNOnMKAw7AXnajTmr304RhxrCgPoK5r3PsVnG/aQQFOpFgrXaUz4NwR0f1xDd8q7Cpv6tBupma9LRBdRRY1TGzAg4Fjna6ITUnTY6/r11PQZbzhvPR9f3Wk+/b7URIO2MZwX7q6ZPoEIfwxTNfkVzWDbbaeiAd5MX5gNCDm5WmEVV7uamvCMFU5fUwS8TvMsBQHCi3v4REeMS3Of+FB3afqmC9Wuo/ExAqb6zFtLs6YLDQII8skQ/CJOXwxbjrslnaq6F/IQnbFegxztE02QYl8TJ/F0cqyuafA4ha3TLNR3Ps9yv08J6vZ0gKd8Sli3NFjYUZr+WxizVt6jHvupDDnRwRk+83XS9JnIGDr3Gh5DjvwIY8v8YFyY2vPOhFVU5nvMZ9dczz0eIcO/0HXSnrYTXTUYCJrdZe9Ix2vFKmTmZRcyrYmF1Hm/cGP4P0eKvq4oXDSoKgjf3XbKMx2JlTR9YOA8x0cmdcIpadpNo7yymnINLPVH+bR/1keJEP72dMQ19YIJlPfWBe7pEUcVF8xhbJB7jsExjN3dUN6LC9Yy+yTIV/tETHN/zEhPv7leT8UPg6OETHldvFuzVQWB9zXbDQLNZkUcG4GBBxs+4OWaQMIgMJahu2EUiaiZTq9xa/ebpzwDI+OC6QzLzsiRJ6conBTiphYp7J1GsI0KcwNGtHbw0UL9YCEVgUoRF/l2hRsDzr0gQKRpq5g48gdUbqrEEcTpVxQEztTTaSzrSuu1274Bn9Ua2jhQsA2ZGn4pW7BK9xPzDGAv1wzsMkNC9EXWTQ+xMonqy+/jnAop82D8YQbPEgSQydybVvwWHnJcinLMN5x7aIC5w6wp5K4t9HIspMsn1kpCptVm8hk5AOKqRaF4PX1H30vpqjVVnX4wPEttvtQN9P0tjpGYdJb8Q0hodWig3ihFkaXrpYxAUsYogYxAcvpXAglhJZAQVgI5DklFP0uIPlWKIj28tKOq9DC0oJA/TX6fYIE2CLT7kW1sQHnvZvQ+OFPpEGW6LzXBg2mBL3RYy8txrBW0ym8S75CZ9pwXHgREdyz1UFZwwpju4Cz03S17e0fyuSZIYxtDBS2S5T3XsKurhNJaDy/+WR5Jo1uZ+u60px3K327TRDu4j/v9L89nxr8fTeNnRcLsW67+bejHc8Mgl8W8ChNN79CswSJX5EULl691BxNYk6N7A9hyUGIJaWjIRTyear8zueRc2rN20gaG1CrEdqHSDI4OeTyGe4A9DTmP8EPezes4WAk+1sHcVdz+PsTDjyW3uoV/cewLqijioIThUhRwWMj7x0kUfTX34Bz/Tj7nZeTS08U75DnhWBpEkZMfGYPkvGb/uzY52DyGpbj7v8Qv+kQXx7pVUxzEzbHeZRxcBVcRkpQrVKkyK7m86YiEGM9olLYe93Utx7jRUSRkjoMDXeZqv5Ccz1ldcW2AIjAJx3IBLNWol9mGX/+Fsnf05ymUj+4W7ywflB9A1krPGO/J5jJ+Z2C3JHdCxINXdvPzYiXnXilFBYIRBo5oig8Vvq7wEp/xh/C5p5P75SdaYXDAmUB/p1AONwqSdO3sFHtL1FXfszO27W0iW5ZmO8llgm4TohDfjAQFwqpIpeRiPg9i18/wIazrSVCDSLydE8IKBuA4D5Kw+lGmsI/NtbmULqW8Ir/sdEVT8hyyjhMKJVyslJ3RvL9Pm7psV+AgNhAZMrLg/51BOexk8c6QfpZyForFIFfgDcqiCWEZQC1+wQhYhEP2aXItEFclqtnC7cALoMIjQeIzFwF5nYYm8nvHczXZ+0BRU5hDYu6l+R1+yBPFKiuwS4qc7fY8CBrAcXorqZg0kaIEDWzB54uVRbWLJooB5OJ1E8Iyg9ZcuBsdNr0mfGkgEiSYovYm6s/fIHtHo3bjNrGcmpsTykvRWdt5DjnoSsd6tye3wMsPepj6Rmp4Xchda7me6T8k4odcBO+EFbRT/Uw7l83Z9uMz3+9oe6gUHd2caIUGWInRmXZ1PjsA8XpXqfBPeH0Ja29O5f+XMX5fHKUSU9Tg5jGm6iT+9k9HpcIRLLu4zkOrO43tLnFphQWs7OeMkR/gsL2NcMTZb3MlbVRiobZRHmvQmvfh1Apf4DiTGDOfYsW+QOtbvn///rnKsfAVfsQvGin0m2nDGeRos4uC7hJuBS25bT4j1lF2i1xejGq0fK+hcD+KXGEkr7fg1ovK1H24rTmhEoXmTx3W+zx6B9zH635OZSOfdq0K5MB9HNu43b82BXp3juE6KgENqTHa426nUoK+ON/xgaCL+/8CDAC+fj5LL33BkgAAAABJRU5ErkJggg==" style="width:120px" height:auto; margin-right; class="header-logo">
        <div class="header-text">
            <h1 style="margin: 0; color: white; font-size: 2.5rem; font-weight: 600;">
                Medical Support Authorization AI
            </h1>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem; opacity: 0.9; color: white;">
                Instant, Evidence-Based Procedure Authorization Decisions
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    

def render_sidebar():
    """Render sidebar with system status and examples"""
    with st.sidebar:
        st.markdown("### System Status")
        
        # Check AI status
        if 'medical_ai' in st.session_state:
            status = st.session_state.medical_ai.get_status()
            if status['initialized']:
                st.success(" AI System Ready")
                st.success(" API Connected")
            else:
                st.error(f" System Error: {status['error']}")
        else:
            st.warning(" Initializing...")
        
        st.markdown("---")
        st.markdown("### Quick Examples")
        
        # Example case buttons 
        for name, case in EXAMPLE_CASES.items():
            if st.button(name, use_container_width=True):
                st.session_state.example_case = case
        
        st.markdown("---")
        st.markdown("### Usage Tips")
        st.markdown("""
        • Age can be approximate ("60s", "elderly", "middle-aged")
        • Procedure can be informal ("heart test", "brain scan")  
        • Include symptoms and relevant history
        • For multiple procedures, list them clearly
        • Use justification feature for denied cases
        """)

def render_input_section():
    """Render the patient input section with improved validation"""
    st.markdown("### Patient Case History")
    
    # Load example if selected
    default_case = st.session_state.get('example_case', '')
    
    patient_data = st.text_area(
        "Enter patient case details:",
        value=default_case,
        height=350,
        placeholder="""Example - now more flexible:
Age: 60s (or "elderly", "middle-aged") 
Complaint: Heart problems for 2 weeks  
History: High blood pressure, diabetes
Family: Father had heart attack
Symptoms: Chest pain, shortness of breath
Procedure: Heart monitor (or "cardiac test")

For multiple procedures:
PROCEDURES REQUESTED:
1. Heart scan
2. Blood tests
etc.""",
        help="Age and procedure can be approximate - the AI will understand!"
    )
    
    # Show validation feedback in real-time
    if patient_data:
        feedback = get_validation_feedback(patient_data)
        if feedback:
            st.markdown('<div class="validation-feedback">', unsafe_allow_html=True)
            st.write(" **Suggestions:**")
            for item in feedback:
                st.write(f"• {item}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="validation-success">✓ Ready to analyze!</div>', unsafe_allow_html=True)
    
    # Analysis button - more accessible now
    can_analyze = len(patient_data.strip()) >= 10  # More lenient
    
    analyze_button = st.button(
        " Analyze Case", 
        type="primary", 
        use_container_width=True,
        disabled=not can_analyze,
        help="Analyze this medical case for authorization decision"
    )
    
    # Clear example button
    if st.session_state.get('example_case'):
        if st.button("Clear Example", use_container_width=True):
            del st.session_state.example_case
            st.rerun()
    
    return patient_data, analyze_button

def render_results_section():
    """Render the results section with improved display"""
    st.markdown("### AI Analysis Results")
    
    if 'last_result' in st.session_state:
        result = st.session_state.last_result
        original_case = st.session_state.get('last_case', '')
        
        # Show summary overview
        create_summary_overview(result)
        
        st.markdown("---")
        
        # Show individual decisions
        if result.get('multiple_procedures'):
            st.markdown("#### Individual Procedure Decisions")
            
            if result.get('overall_summary'):
                st.info(f" **Overall Assessment:** {result['overall_summary']}")
            
            procedures = result.get('procedures', [])
            for i, proc in enumerate(procedures):
                create_decision_card(proc, i, original_case)
        else:
            create_decision_card(result, original_case=original_case)
        
        # Add save/export functionality  
        render_export_options(result)
        
        # Show diagnosis details
        render_diagnosis_display(result)
        
        # Analysis timestamp
        if 'analysis_time' in st.session_state:
            st.caption(f" Analysis completed: {st.session_state.analysis_time}")
        
        # Technical details (collapsible)
        with st.expander(" Technical Details"):
            st.json(result)
    
    else:
        st.info(" Enter a patient case and click 'Analyze Case' to see results here.")
        
        # Show sample output
        st.markdown("#### Sample Output Preview")
        sample_result = {
            "decision": "APPROVED",
            "confidence": 95,
            "procedure_type": "Cardiac Event Monitor", 
            "reasoning": "Patient has symptomatic palpitations with cardiovascular risk factors. Monitoring is medically necessary.",
            "urgency": "URGENT"
        }
        st.json(sample_result)

def create_summary_overview(result):
    """Create visual summary with clickable cards - improved"""
    if result.get('multiple_procedures'):
        procedures = result.get('procedures', [])
        
        # Calculate counts
        total = len(procedures)
        approved = sum(1 for p in procedures if p.get('decision') == 'APPROVED')
        denied = sum(1 for p in procedures if p.get('decision') == 'DENIED')
        pending = sum(1 for p in procedures if p.get('decision') == 'PENDING_ADDITIONAL_INFO')
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="summary-card summary-total">
                <div class="metric-value">{total}</div>
                <div class="metric-label">Total Procedures</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Show All", key="btn_total", use_container_width=True):
                st.session_state['show_procedures'] = 'total'
        
        with col2:
            st.markdown(f"""
            <div class="summary-card summary-approved">
                <div class="metric-value">{approved}</div>
                <div class="metric-label"> Approved</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Show Approved", key="btn_approved", use_container_width=True):
                st.session_state['show_procedures'] = 'approved'
        
        with col3:
            st.markdown(f"""
            <div class="summary-card summary-denied">
                <div class="metric-value">{denied}</div>
                <div class="metric-label"> Denied</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Show Denied", key="btn_denied", use_container_width=True):
                st.session_state['show_procedures'] = 'denied'
        
        with col4:
            st.markdown(f"""
            <div class="summary-card summary-pending">
                <div class="metric-value">{pending}</div>
                <div class="metric-label">⏳ Pending</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Show Pending", key="btn_pending", use_container_width=True):
                st.session_state['show_procedures'] = 'pending'
        
        # Show filtered procedure list
        show_procedure_list(procedures)
        
        # Overall status message
        if denied > 0 or pending > 0:
            st.warning(f"⚠️ **Action Required:** {denied + pending} procedure(s) need attention")
        else:
            st.success(f" **All Clear:** All {approved} procedures approved!")

def show_procedure_list(procedures):
    """Show filtered procedure list based on selection"""
    if 'show_procedures' in st.session_state:
        show_type = st.session_state['show_procedures']
        
        # Filter procedures
        if show_type == 'total':
            filtered = procedures
            title = "All Procedures"
        elif show_type == 'approved':
            filtered = [p for p in procedures if p.get('decision') == 'APPROVED']
            title = " Approved Procedures"
        elif show_type == 'denied':
            filtered = [p for p in procedures if p.get('decision') == 'DENIED']
            title = " Denied Procedures"
        else:  # pending
            filtered = [p for p in procedures if p.get('decision') == 'PENDING_ADDITIONAL_INFO']
            title = "⏳ Pending Procedures"
        
        if filtered:
            st.markdown(f"<div class='procedure-list'><h4>{title}</h4>", unsafe_allow_html=True)
            for proc in filtered:
                decision = proc.get('decision', 'UNKNOWN')
                name = proc.get('procedure_name', 'Unknown Procedure')
                
                emoji = '🟢' if decision == 'APPROVED' else '🔴' if decision == 'DENIED' else '🟡'
                st.markdown(f"<div class='procedure-item'>{emoji} {name}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

def create_decision_card(procedure_data, index=None, original_case=""):
    """Create clean decision card with justification option - improved"""
    decision = procedure_data.get('decision', 'UNKNOWN')
    procedure_name = procedure_data.get('procedure_name', procedure_data.get('procedure_type', 'Unknown Procedure'))
    reasoning = procedure_data.get('reasoning', 'No reasoning provided')
    confidence = procedure_data.get('confidence', 0)
    
    # Determine card styling
    if decision == "APPROVED":
        card_class, status_text, status_color = "approved", " APPROVED", COLORS['approved']
    elif decision == "DENIED":
        card_class, status_text, status_color = "denied", " DENIED", COLORS['denied']
    else:
        card_class, status_text, status_color = "pending", "⏳ PENDING", COLORS['pending']
    
    # Display the card
    st.markdown(f"""
    <div class="decision-card {card_class}">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem;">
            <div>
                <h3 style="margin: 0; color: {status_color}; font-size: 1.4rem; font-weight: 600;">
                    {status_text}: {procedure_name}
                </h3>
                <p style="margin: 0.25rem 0; color: #6b7280; font-size: 0.9rem;">
                    Confidence: {confidence}%
                </p>
            </div>
        </div>
        <p style="margin: 0; line-height: 1.5; color: #374151; font-size: 1rem;">{reasoning}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add justification for denied/pending cases
    if decision in ["DENIED", "PENDING_ADDITIONAL_INFO"]:
        render_justification_section(procedure_data, procedure_name, original_case, index)

def render_justification_section(procedure_data, procedure_name, original_case, index):
    """Render justification request section"""
    justify_key = f"justify_{procedure_name}_{index}" if index is not None else f"justify_{procedure_name}"
    
    if st.button(f" Request Justification Review", key=f"btn_{justify_key}", 
                help="Provide additional clinical information to potentially change this decision"):
        st.session_state[f"show_justify_{justify_key}"] = True
    
    # Show justification form
    if st.session_state.get(f"show_justify_{justify_key}", False):
        with st.form(f"justify_form_{justify_key}"):
            st.markdown(f"**Additional Justification for: {procedure_name}**")
            
            # Show what's missing
            missing_info = procedure_data.get('missing_info', [])
            if missing_info:
                st.info(f" **Consider addressing:** {', '.join(missing_info)}")
            
            justification_text = st.text_area(
                "Provide additional clinical justification:",
                placeholder="Example: Patient has contraindications to alternatives, emergency circumstances, additional risk factors not mentioned, recent test results, specialist recommendations, etc.",
                height=100,
                key=f"justify_text_{justify_key}"
            )
            
            col1, col2 = st.columns([1, 2])
            with col1:
                submit_justify = st.form_submit_button("🔄 Re-analyze", type="primary")
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state[f"show_justify_{justify_key}"] = False
                    st.rerun()
            
            if submit_justify and justification_text.strip():
                handle_justification_submission(procedure_data, original_case, justification_text, justify_key, index)

def handle_justification_submission(procedure_data, original_case, justification_text, justify_key, index):
    """Handle justification submission - individual procedures only"""
    with st.spinner(" Re-analyzing with additional justification..."):
        justify_result = st.session_state.medical_ai.justify_case(
            original_case, procedure_data, justification_text
        )
        
        if justify_result is None:
            st.error("❌ **Error:** AI system returned no response. Please try again.")
            return
            
        new_decision = justify_result.get('new_decision', procedure_data.get('decision'))
        decision_changed = justify_result.get('decision_changed', False)
        
        # Update ONLY this specific procedure
        if decision_changed and new_decision == "APPROVED":
            procedure_data['decision'] = new_decision
            procedure_data['reasoning'] = justify_result.get('reasoning', procedure_data['reasoning'])
            procedure_data['confidence'] = justify_result.get('confidence', procedure_data['confidence'])
            
            st.success(" **Decision Changed to APPROVED!**")
            
        elif decision_changed:
            if new_decision == "DENIED":
                st.error("❌ **Still DENIED** - Additional justification not sufficient")
            else:
                st.warning("⏳ **Still PENDING** - More information needed")
        else:
            st.info("🔄 **Decision Unchanged** - Original decision stands")
        
        # Show AI assessment
        assessment = justify_result.get('justification_assessment', '')
        if assessment:
            st.markdown(f"** AI Assessment:** {assessment}")
        
        # Show what's still needed
        still_needed = justify_result.get('still_needed', [])
        if still_needed and new_decision != "APPROVED":
            st.info(f" **Still needed:** {', '.join(still_needed)}")
        
        # Clear the form and refresh
        st.session_state[f"show_justify_{justify_key}"] = False
        time.sleep(6)
        st.rerun()


def render_justification_results():
    """Display recent justification results that persist across page refreshes"""
    if 'justification_results' in st.session_state and st.session_state.justification_results:
        # Show only the most recent result
        recent_result = st.session_state.justification_results[-1]
        
        # Show success message with details
        if recent_result['decision_changed'] and recent_result['new_decision'] == 'APPROVED':
            st.success(f" **Decision Changed to APPROVED!** ({recent_result['timestamp']})")
            
            if recent_result['approved_related_count'] > 0:
                st.success(f" **Bonus: {recent_result['approved_related_count']} related procedures also approved!**")
                
                # Show which procedures were approved
                approved_list = recent_result.get('approved_procedures', [])
                if approved_list:
                    st.markdown("**Related procedures approved:**")
                    for proc in approved_list:
                        st.markdown(f"• {proc['name']} ({proc['old_decision']} → ✅ APPROVED)")
                
                if recent_result['related_reasoning']:
                    st.info(f" **Reasoning:** {recent_result['related_reasoning']}")
        
        # Show AI assessment
        if recent_result['assessment']:
            st.markdown(f"** AI Assessment:** {recent_result['assessment']}")
        
        # Add dismiss button
        if st.button(" Dismiss", key="dismiss_justification"):
            st.session_state.justification_results = []
            st.rerun()
        
        st.markdown("---")


def render_export_options(result):
    """Render export/save options for results"""
    st.markdown("---")
    st.markdown("#### 💾 Save & Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Export PDF", use_container_width=True):
            st.info("📧 PDF export feature - coming soon!")
    
    with col2:
        if st.button("💾 Save Results", use_container_width=True):
            # Save to session state history
            if 'saved_cases' not in st.session_state:
                st.session_state.saved_cases = []
            
            case_summary = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'result': result,
                'case_data': st.session_state.get('last_case', '')
            }
            st.session_state.saved_cases.append(case_summary)
            st.success(" Results saved to case history!")
    
    with col3:
        if st.button("📋 Copy Summary", use_container_width=True):
            st.info("📋 Copy to clipboard - feature coming soon!")

def render_diagnosis_display(result):
    """Render improved diagnosis display"""
    diagnoses = result.get('differential_diagnosis', [])
    if diagnoses:
        st.markdown("---")
        st.markdown("#### 🩺 Differential Diagnoses")
        
        st.markdown('<div class="diagnosis-container">', unsafe_allow_html=True)
        
        for i, diag in enumerate(diagnoses, 1):
            name = diag.get('diagnosis', 'Unknown condition')
            icd10 = diag.get('icd10', 'No code')
            confidence = diag.get('confidence', 0)
            
            st.markdown(f"""
            <div class="diagnosis-item">
                <div class="diagnosis-info">
                    <div class="diagnosis-name">{i}. {name}</div>
                    <div class="diagnosis-code">ICD-10: {icd10}</div>
                </div>
                <div class="confidence-badge">{confidence}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_footer_metrics():
    """Render footer metrics"""
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("~15 sec", "Response Time"),
        ("Transparent", "Clear, Structured Justification"), 
        ("Faster Approvals", "Saves Time & Effort"),
        ("Scalable", "AI Support for Doctors")
    ]
    
    for col, (value, label) in zip([col1, col2, col3, col4] , metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{value}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; color: #6b7280; margin-top: 2rem; padding: 1rem; background: #f9fafb; border-radius: 8px;'>
        <strong>Medical Support Authorization AI</strong> | Assisting healthcare authorization workflows<br>
        <em> Demo Version - Built for real-world medical scenarios</em>
    </div>
    """, unsafe_allow_html=True)