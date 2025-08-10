# ui_components.py - Clean UI components separated from logic

import streamlit as st
import time
from datetime import datetime
from config import APP_TITLE, APP_SUBTITLE, EXAMPLE_CASES, COLORS
from utils import get_validation_feedback
import json

def render_header():
   """Render the main header with modern sleek design and logo space"""
   st.markdown(f"""
   <style>
   .modern-header {{
       background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
       border: 1px solid #dc3545 !important;
       border-radius: 12px !important;
       padding: 2rem 2.5rem !important;
       margin: -1rem -1rem 2rem -1rem !important;
       box-shadow: 0 4px 20px rgba(220, 53, 69, 0.1) !important;
       position: relative !important;
       overflow: hidden !important;
   }}
   
   .modern-header::before {{
       content: '' !important;
       position: absolute !important;
       top: 0 !important;
       left: 0 !important;
       right: 0 !important;
       height: 3px !important;
       background: linear-gradient(90deg, #dc3545, #e74c3c, #dc3545) !important;
   }}
   
   .header-content {{
       display: flex !important;
       align-items: center !important;
       justify-content: center !important;
       gap: 2rem !important;
   }}
   
   .header-logo {{
       width: 80px !important;
       height: 80px !important;
       flex-shrink: 0 !important;
       object-fit: contain !important;
   }}
   
   .header-text {{
       text-align: left !important;
       flex: 1 !important;
   }}
   
   .header-title {{
       color: #212529 !important;
       font-size: 2.8rem !important;
       font-weight: 700 !important;
       margin: 0 !important;
       letter-spacing: -0.02em !important;
       line-height: 1.1 !important;
       background: linear-gradient(135deg, #212529 0%, #495057 100%) !important;
       -webkit-background-clip: text !important;
       -webkit-text-fill-color: transparent !important;
       background-clip: text !important;
   }}
   
   .header-subtitle {{
       color: #6c757d !important;
       font-size: 1.2rem !important;
       font-weight: 400 !important;
       margin: 0.8rem 0 0 0 !important;
       letter-spacing: 0.01em !important;
       line-height: 1.4 !important;
   }}
   
   .header-accent {{
       width: 60px !important;
       height: 3px !important;
       background: linear-gradient(90deg, #dc3545, #e74c3c) !important;
       margin: 1rem 0 0 0 !important;
       border-radius: 2px !important;
   }}
   
   /* Mobile responsiveness */
   @media (max-width: 768px) {{
       .header-content {{
           flex-direction: column !important;
           text-align: center !important;
       }}
       
       .header-text {{
           text-align: center !important;
       }}
       
       .header-title {{
           font-size: 2.2rem !important;
       }}
       
       .header-logo {{
           width: 60px !important;
           height: 60px !important;
       }}
       
       .header-accent {{
           margin: 1rem auto 0 auto !important;
       }}
   }}
   </style>
   
   <div class="modern-header">
       <div class="header-content">
           <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACbCAYAAACAn2I8AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyRpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDcuMC1jMDAwIDc5LmRhYmFjYmIsIDIwMjEvMDQvMTQtMDA6Mzk6NDQgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcE1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIiB4bWxuczpzdFJlZj0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL3NUeXBlL1Jlc291cmNlUmVmIyIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOjA5RDc5M0JFMTE3NTExRUNBMDU0RThFMEQwQUIxRUJBIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjA5RDc5M0JEMTE3NTExRUNBMDU0RThFMEQwQUIxRUJBIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCAyMi40IChXaW5kb3dzKSI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjE5MjBFOEUyMEZCNjExRUM5NTI5QTg0OURDMjM0Q0Q3IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjE5MjBFOEUzMEZCNjExRUM5NTI5QTg0OURDMjM0Q0Q3Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+AjpEsAAAOQdJREFUeNrsXQeAVNXV/qb32Z1tbKEuAhYQARGxKxbAEmtE0NgjUbHF+CuxJcYeo8YakdjFYMGOooL03kE6KrCwfaf38n93ZlaG2Te7M1uoc/WxuzPv3frdc75z7rn3yZCQSqGU34XcMZfCOFoJnBIB9OJzDWS/zIHn0/nwfvERXIt/RsCBbMqmZpKs8ZezoO/yMPJe7QPV2R5ElMk3Knkrb/bUILR5NXwLl8H/40r4Fi2Gd4sV4XC2K7OpCbAGQJM/FaU/qoC+LkR2o00iKXhpIed/QAgRbzVCa9fBP2cq3D+sgH/pCvh2BphHNh3iwFITRq+i8OFLYHzIjnDGqFTwXzV/yvnTj0jdLwgsJ7hmroZ/1rdwr9yEgC3bzYcgsMqh0k1FyVwT5ANC7SD+VFGgyaISjSryV0qzxcvgm06wzZkJz4YqhPzZbj8EgNUZyh7fonSxBfL8UDtnLo8R/yg/YwpWIrh+KQFGoM3gtWgJfL84kKVnByWwLodxwFMomEXuZOxoZiQApo0ZAYKfOSoQWk2JNpP87Mfl8C6j+qzNwuwgAdajyD/9Rpi/8iGi29uFN6pNATQvwrs2I0hw+WZ8DfdMWpw/bUfQnR2iAzMpSbgj+8qGE9ZjowVJcJX0gercflCf+3sYQUNiIyXYwuXkZ7zmzYF3cx1CWYF2oABrf6mIgBelZvSSRV0ast4nQdv7VOiuEgKtAsG1i+CdtYyqcxm8i8nVdnqzbo0ssDIFmTAk3NHfouDR5kEx6CIYeeHOICJ1mxFYMQuemSvg/5GGwKr18GfdGllgZZ4IJjh2S6j8HlANOwLqYTQCBAB/3YDAYvKz6eRnc8jPsm6NLLBal8gNo1fcrdHtaKi7DYLm0tEwhWwI/7QCvrm8fqTKXDQf3p9tWbdGFliZpnDUqoxEL/IzhQGyfsOg73cW9GMJPec2BFfOg2dWHGjLVsJfm1126mB3w0PIO+1m5Hzt3wfuhr3p1hD+s0jMEt21Ef5l0+GZQatz/ir4N29DoM6DSCgLh6zEarVbg6nkSGjOPRG6c60I11OavfsI6l/7CM61WThkgdU68czLQEZWRdX4HJwvfQv3V+vgr7Rnw36ywGptiq9beqbA+cADqH+hAsG0rca+UBtrECIgQ84sZLLA+i2JGDI95Nv/irpRL8E2L9PndZDJb0LOCb2hGrgMvu3fwf0DVejOrKXZTJ+fBl33wdCOCQmOe5BKKqq/XQTVCIJqaWvy2ImQbyY8mwOA9W5YbrsLuc+NhH74ydD1zoFCzY6z2xFx+bOW5qFhFQpOZYQscD/qR7wI2w/tkWcOofoBiv/FCXknLcmoyHcgXFeN0PJF8M2nRJu9HD4R7Fh7KAPtoAaWIOrT4X72UlTe1Z755jLf99DpGVqWd4moWwVikbSNLg32ZZWIpF0F/xxec6fBvXoD/HVZYO1XJHB3DBdivtBGf5Oq8QMf/xUfRpJUIFP16dh51Eb4a9u7XrlQyD5H8adHQXOBO4lrJUfSkotV0PpcJqTZilikxupdCNoPZoa235J3ASZKgeBOBDkQnm+nwr2S4K+EcEvFxs5yFNRlx0J77DHQDLFAPoDPaL3xpR4hrT6E872OAJVIVoQi96Hupo9RMojgKUsESVxq/bbkRIlWNgiasiHQni/+bkBo+wYEFhFss3+AZ8Ea+NfsQNAVPIhU534nseISKrQGvrdehv1FqpHldWjeKV7EoesLde8RMIw4FdrL+0A9VORzBSqHfg7Xgo6s79+Qd+VtyH3HmYGFKFSnOh6yLWYI+dmvBNb8BfDOngfvvPXwb9iEgCcLrHZIkZhZDxciG/+Jhj+9Dvv01sRbGSmpLoPxrOtgvvB6VD9AiVXfkfVmebJZKJtdBuWJrSXrigSVT6kVsSK85WcE5xJk5Gi+hYvh++WXA2yT8H4BrEjMesN2BGeNQdUoqoZd7WUV7g3lMhY5I59G/lfWdvJryeMSTR0HGq3PnynN3huH2id2HSDh2vL9hU9tQ3Dh5ai6sL1Ahb0EKpHeh+Mbqq+l6ma3+qafGqM1hMVJUMmYa/k50D8wGcWfd4ZSnwVWmhWgBbXrNtRczsFpOBD5hFhr/A6eidp2Alby5AhHCX9Y7Fgf9i8UPCDLAis9X9NDqL95Fry/Hshk9Wu4p9BctXXUoMtilijOgO6WE6EtywKrmSTIOk3u/70K26cHunm9BN7KzfD/qELHyZNITLqbLoDhvCywmik4gIjrXtQ9dDAsfQhONAOez7ToWEUl+upYaE/MAislYZdjEXyTxXkOOEjSVLjnhsRCQAcnguuwLLBSFxz6GM6XcRClLQhsrURwU0cuZ4hI2F5QFfSGSpUFVlISPGQHgounwLX0YAJWBYLBKoTWaDuwW4WFaIZczUubBVYTNSiDOHrSifBBF1fyDdyTHAivNrFrDdFTwzoEXJEw9m9iKm/vzJTxNbDmrygf+WFv9Ewu5LKuUGr2Voc+iYbPT8aOAXeh9qTv4J6ogczb0YR+f0xtogNijUsTDQ2JgcWJiLsBISt/FREFwtnpieMtEv+Zy38s/NLxE/zrOrpxf4T5hNuR+0wO5Kbv4fn2Qzj/+z3ca30dPNl/RTD0X9jniusU6J59FHl/7wvNxc5DKJQ547XCRjAJyVOD0MbV8C3dhdC8ufCuY4duXgtfI6ACUkJNBpmWZcnZyR26MeEkaAu+QMkyVqKLILw64prg96yCb9IE2J+dDOcaz17SJgb21WPIH3cdzP+0Iqxu04DFOOovI7Cz3zL4nAe8xBJgElcdQusJoilUZV9S1K/I8AwrMWX3yiLqadBdxAHo0iglXLGfuj5QX/dvFI7+I3Le/zesz/0PztUdXRdxYPDtqH2BsNh+HUzvE1y6g11iNQusSBxQcQ/595zp/5kOz9dbEdivV9hFmPBQaI+RkkjxrfjaPlBd9zKKRo2EYeLLsD23EN6tHV2vO1AjVhjGXg3jW46DPB6+WfJu4dc7EVxwN2pHDMPOs16H/aP9HVSNEyIfivLmGI0AnQdh/e9gGDcVpQvug+XsvVEvguvtGfD827R/BJbsXWAJMcaGO96D867zsevk12D/5kAiniTrNANl5ZE0BlocrksyX3gHcl8/HOrcvQGue1B3PynFZuVBbC3KkxutZ2NJeBdfi6qTx6L62R0IBg+0Rh0DdVk3KIvTPVEmGCX3si5HQT10b9RvEwKctI5/GA4VYIk9c0vgmzwSO4dNgWvlvqrUeTB0fxedbr8GpnOLoZC3QiqIsBJzJs8IeXwOdF1bU99zoT9C1PdamM4ojtrNLSdqgclVlFqKgxRYjeRdZiaoFsD74hWovKMe4X12pM8gaEo4SD+IqEnyHxGuvOQtOF57C/b3KhFypwmSXVSFPlpjGTlGd8V8cBmlS2Hs9QaKZrLDCuP1nfM2HC+wzlN2IRhI9Rw1gWc+vJPPg3686yAk8nKKA7kRMi2tordGo2rcvgSVUAy3I/dqdnO5CMsVMeR5UBz7V1hem46yBffCcl0RFC36gRbD+/MbcPyFxoddl6a64V3B2fBuzLTOf4T5Fj85mmN3fU8aD8v/fkDpXBoEF7K+KSvwFVyfyXBwmofRVZj1CHx9Bapuammb1d4gtj2hOiaRG4nfbbEB68cBmzgDZXM4YJc2Bxhh8d2GmheuQfWgFfAJC8zR3P1CHdUjVEsLeEumdVZBNiix1xLqO5j1nPIjymaw3sOkyp8H7xoC8teD0T6UvwvH8nGouYGg8u3ryiijaixSLvVd44Dlc8AeQt6Hr6HoUU0zYBGc6SM4N5+DnbffGAWYXwDMJjXAwu9VS76zAX57JvXtDbWORkJnKSMhAWCnPoi8719H0Z3JZddQtf+EwEZtBy1W71Ng0UKp4czJeGdMH6jUz6Pgjj8jd3QnKNrFk3wMNLm9oOrcXESpGDBxVtVFMIwnyR/YUp5CmnwI56ZzUHH79ag+biX8LyYDTITxOBFZn+nw0tgp5VXYnCNG1JegxUgYHh0ATbfE74Szthqh1ZRYHnnceBKXdvf7hw4uP1Y66WqYrr4Nuc9Serz3A8rm3wPLNflp8J/mkhqycg5ycTqkQ9xTDlXa7gEBsI/h3DgcO8fFAOZ70UAVmRvrAutzsL6R6YG3x0DdRwaZIZ26UhrrToLu2OTv7kXd34Zg+1HnYVffv6H+zH+g/tZl8E20IrSlEWQHslWYMclmJ50kJIeIFCiAov/9sLxBc/vmp2Ed9ybsC8OtQ7mH6k3mTnOAI2IZLsMkwCMA9jlc44ZC+/xw6Pt9Adfa+a0g7pR8ntju7fTcGW6JhXfyOrHDObrLmYAS56D+8BTNgM5QGq6C6fQzobtlELTDBW88kM52aLXEkgmKkcQnCsl/HkHexBIoW6UaaUSsnwXPo5QiweZmqvhGqMsKBFe1tv6izixr83jUTWkNqESaAPucH+B+LbcFySI62UVQTYcn7VAhcUjI42j48hzsGvEYGi4Tpz1rDiDp1VpgiTez5iZvdRLSi3MqXyGCRFuRyEUiF6Hy/ptRc+IGBCaZIQ9IDVjsbWGR6gXwbtuXnUeLLnAJKm8ai5pT1sP/Kesbkaqv6GQ7wtt4VWZahpBST6Hho6tQdYoH4ZUHCrhaBSyCJ/Jv2G5qQGhGTjTOSfYbCf4Fgc2UXtbWVkiA8x04Fp2FitG3ouYkWmr/MydJMGVUhYS2c6Dq93UHivq+B8fss7HzoltQczoB9nkywMTWe7Zjy44MDtRNTuKoyj+g+kIXJxT7W4uDOZEHgOT9/I3o9qMd5ZEADot8gOIJ7VmG4DA0FAbPQecPbCgP1bMcP3qKcp7riDaVsU2XwHjaE8i/cTRMo4dB10efgZQQgPoDTKfMRtlnrG+kIdovPSMvofDu9qjfX2D5vQ89dw6ExoSDPXXhYDyMvAumovS1MTD174gyNLEBO+5jFL8yGcX/7A9NfnuXQSLfZTO6feOIA0JMllr08CxGlxlPo+CmAdCUZGDhguT7VNZ3wocofrAXVO3ikqHlLduArv8ZAm3x/oyJQy/KP0XqDpVhBkp/oKU3JDFAsPHYRyE5qXpr11LVTYT9DRL/OZX7aKXiKRQc/w1cW2gM1GSBtZ+nN1B070UwPt7cy88bX54uPPXVCM55D84J5FefbUFgr74rsRRKGa1MmW0/fqNGFlhRaaU0TUPpaiPk3dKVQcrdUuyXOfC8/QJs7y6Cd1P2TU+xpMh2AXADzGecD8Mt7gwckEJU+GPnvOceAc2pl8J43QUwHMG5Wr0Zge3tddDJH2E+/XKY7j4TusFyyOq3IlCdBdYBkk6FbszJ0J3WmjNPG09I5k91MZRHnwvDtWdBf4IFckc1Qlsb2qCu7kLuhU8j/8tB0AwZDO1pBO51zL8/JevO9QSvbz/2xB/ywBJ86c/IvbQEyuPaGoMtnudgyzpB0ZPgGnUJjOeSD/nXIbDKkeFxAt2gNL+EwilEZZ47/pJP/q5kPY88B/prCbLBtDx3bkDgl/0RYAdkKFB7VlqQTEqawvZkwWKgRdCfFrKB45D7xico/qorlAWZ5HEBjMcToD0CSdLRG1s+k5VBee6jyJ8xA2UfjkPOUMN+NpQHFLAOg0r5JPLHsjNfewT5tx0DTWl75BtEpLAj6iuIvAiZ6Q318MkonpzJGRJUJUc0B3Z/fH2WALv0CRTM/hjF71BK9suqwgyT8CV9iOJ/kyT/zQz5oJOhHXERjFeTH4n4ra2bEKxrjdSJQCa7BuY786Eo7giLThaXYLQ8e5AbWb+Ge346z90Dy5VdqJ4DaYCXqlJO1Xn0FTD9gf1knQXP4qzESjMRUMcPhOaWxlAda+zlSAWnQHfbf9Fp0bcofV5sbMi0QUVQaHMgz+tIh1DsYNow1Zvh9nKo0lqKyYX8sHAG+QunrhNhw72wvERL8pRDAljC33MCtL37QNXqZQhKpsukTH5xJgOJcU5/qG97HUVLvkfZ82dD3z3dfI+EKqcLFPqOjnWKH5jWZST0J7d0bw+oFFRx5ZkGHsZjvnA1zOP2dQTqXgHWVTANm4my5dNQtuJLlDyVycCLJLajU1od3tzpMOI7AsxM3nXbWyha9iqKHu0PTYvciaomNywOhNkLSRaz9oa0dF8xFN0LIS8NtRLAShHcuo9pjnxvdOa5MFxMoqlngzudCN1f3kanJS+g8GGS8Zw0s1EaIeuazvwVEoydaxkF4/hpKF04GqYTW5CmYjF7r4ShCHeEkERpSBNTRLwFpvXSUXPQA0ukAiiifEFczui7BSP518P00AfoNIGkucUOoNlt0UDWOZLBrI2v+fV4GvkfULWkNPWHQ3f43lIbghsOgMbcUhx7HcK/8t4dbUCGNY7jgxtY7KBeyQMvXuFRAuXplEQtSq2joelGkm0OZcg5hElONdr5ZuRcnOoeA+TmvdXZAig0PnwtqbiN8De8Bvs4crJafStAzyfWxrv54AbWMvjeZSf5E8Nq5TGpUsHBb/F1aUdA3TfUyrrGj68+NtX36+Bfv7dormj/PHgrPGmM+cOo//RyVA2YD+8TBH+dfvdbZptN8YOD14b2sTe+w4Elmncnah+8BTXHbUHg7Zw4wMQmzVXwb6pEqCVXDfpBXdSW6UeLL6VU/AruueRlv+4tQqIGtqd771dw7TgPu+67ClUDF8D3BMFV0xLAxHfs09X7epFnr0gswS0mwr7yDFRcfQdqjxcAY8HbtiP4cTod8AVcc/Vt4EFhseklRdqMgP1V2P9PHIqi2AuTbBdCP2f6HAG27VzsvG8MqgYTYE/qIa/Rp95kEpwBz8Z9jKu9azkINrkcvspJcHz6AZxvToFrSToMkwDc3htqlXj3s1iIzcQMF4faEjivUR2vSHXPTKoOFWQ7BkEzkJzMHOoggiJm8aOwPrsTwYrWPM9JYGPffb8Gvv8VQ+nvCdWRrLeuUeTHjiiQbXsFtsfJYQOHDLASfEeoR9ibrtkiFl4ptaYTYF/RwtN3hvJIUfd0ACZm9idwPbka/h3N3UdwLf8a7nfUkG0pg6IgD4ouynY2rQgC1//gFIfZtWl30SYC7H04v1+LwKQSKPzlUIsNHwYFZLY3YL9nMpxL9rXEOuAiSMUq/igYj7kB5juPhHoU1aw6VdiIIno6YbhhOHb1XpfB2+zz+eTvYTz9XOivHwLt75SQGT1RN0lb+ZWs4nzsOmoRvO0ayizWS6nK+1YjtGkhvFv2h3E6YEOTxTLRaJgG3gjz7QTY5ZRqmmSACf+UFaFlx2PH4NbGh58OXR+CeMxgaK8UYSzCwx9ohcUldu1Q0qw+HRVHBw7yE5P3mSpsR762i1ztU6rIqeVUkV2gPLxRRYqhE4Sc5v3Xk+D8rLVD+QuCdVSlM76E603msUY4a4ug7E6+JMtEgimjZ+SHl78O+3s4BNIBH0EqnKBxgE2piHEwAwHWhypTSSm17j7U3f4zArVtLceKsO97eFaT27y1DYFpXaGUFcZCYbTpkH3hX6IB8fXHcH1zKADroNulI04iHgZ9X6rKkg0ILFwBn70jyhHxYbQiu11PNXkC1STBfIQwMlLxvTxKzxtRc/r7cPyYBVY2pZVKodSSh40YAf0NfaA+O4yIMoCY118RV8lz4X3rMlRe4ziEXtSUTQmpCArB1Upacwa7UHe0Jgd9h9Ln16HbegfK63ag+7bPUPJ0YTudephNB2C6EIYBv6L7um3obl+Ezh/ehJwzWvtqkmIo1COhL6bFasr27CGcCCD5EnSeXo8ekQp0j1TzpzgUhACb9keYh5sP8nffZDlWB6XeUJf9gNIthI8mkQXFFsxl4rTBryfA9gStwtmuLE9qMWWnYTydCG33HMg1yZDxxbdZdYdy5LMomDkFxa+Qh2myPZYFVlpJKQ5hbiYJgDUgLBsK7dgJKHpQlRX2WWClk86C/qh0llrEdveuUF0hF66sbMoCq6WUC3lpuss+gdjLn7IHqmSB1XL6Hp4vxbHa6jRUnBKyX6La8QBJwgChVbtXJ0J21sXTCvjX1iG89DCoupRA2U1IL6lFZlUsSmEqrcMv2mob9oDK+Cjy7x8Ebe/4adPtDtZ+0HT/FMWTxiLnzn5QF3oQ+flnBO3ZEd/7KlF2O3J/twJdZgo/VhV6RLaj+2+X+OwR5I1rj7JeQeHdIRwWEYfpbkK3jX9H3q1lYgtlOyUjZLJ56PyFOL25ku2wxQ7rrfsQxY+fAV3n7Gjvg5QPhfx25Fy0El1nNwJsJ4ElQHAdzKe2RxnfoXRyTRy4u+IO2a3otqa9zl44HpoeVvTwJE6MHbyEE5jl1giAnQZdSUf0X5ZjpUh1CIWfh23KGag4+SHUX7wTwdl+wEU1MvlbuBe2NX8LFAozFH0a1Wkw7i8jFzrqHlheKG0HX1k3qMTu8T12eQsV74pFYRQMg/7eT1Gy+BkUjGtvIPz2kiaVStVbFg1HlxmDoeAv4XBYcr+fXC7XqtXqrgG/f0so3P5vY5XJZFApVeWsQ3UkEnHpdbrefr//10Aw6M2IPCoUBoVcnu8PBLalc69apSr1+nybWWYkCWB4FtYpr8M+xQh5sRvhSls7eN6LWGo5lJpkS1T4y8QmWhPkKrTxHZJDoe2piBojTe3dGMDCQrKU/Qk5/3YgbH8Y9W+1q8QSg1loyX+zU0HhfzoVFs7QqDSnp+QgZvMNBZa8z2UyeYd4CDnIvTsVFCxVKZVdDHrDafm5ebMIkIx3K+db8p7l9bxoW4tcRK8fb8nJfQfNvEZXhLvsQrBdQCXSBvj9D6D+mhqEvhKvjWl0uAoLbiV8WygZnW0dWB3k/VqqrfjexsnzB5gFv1O0q8QSk7SmvvZSIky868UUDAZ/aUai5PJ+LTpuC7eO+ecK7SCXyUz83RBpRVmsZyc+m+5r8/J57153eL4K24JP4DzvKpjOuAbmP3eDcqQ2dsT3qraeuiw2nQyGplc655MKtcNyC3mJ0B5nuwGL0iHPoNdfycHoGRHnqCJSbXc4nglHIt64+is0m0yXOZzOiRwAf7IlrtNqh+i00fOrikKh0FSnyzkp1MzeBbk8KigVVLchtUrdW6fTnWp32P/LvBujfIMJE6q16jaYyCG1Gk051eqwUCjsdLpdn7Ge7qR7w4nqWK/TD9Oo1RfxT30gEPjM5XF/Fu6A8/qr2bxnYJ3+NhzTCa5hp0B7zkTY2/w+InH4ynx4Z49FzrmVbF64eb8cqhDa4UTE1V7tkstlcoUl1/Im1c69HOQIQTKAv49n52oT+NdJZoPxJX6m2GMA+F++xXJnQV7+Ao1GcxYB2pkAfD/XnPNkowriT5lBpz+W+XaNg7g31e1s/uwu/uZgX2nQ6R7uKAkopDHLOKowL38hwf+IyWh8g6p8EsGdUuxbcnKeZru+J+8azLb34d+f5pjMd3Wk9BInFT6Nhh/Ox657aBxsanO7eZEbPvcf2O5lx24XYT+pCLpwCm+Ef3UVgu22fUiuVCgO4yCfZbPbr62qrRlrdzqeQ1OvcojSy53MQcTp5iS8a1xu111VNdX9+fwZTpdrPCXQn5VKZdSM5eCYxSAReKfEgVaiVChPapQmHPiAIOkdNWAx6aO7mxLUWl1XW95gbbiAE+gCSqOjUz3j9wdWWm22G9meIVW11Se6PJ6XOTHuJ//TH0iW7WYEfDej5skR2DnwPTjui6QAmCzK+QIr29XdoNNpu7LzA6FwaEN8oDVxAIUTZn1IYkJEQeZyu7+rt1qfbVQTbo9nMvOTq3cPnJzPy3g1qreQAFMqopxwn6wdZm04amWqVIOCodA0qjQ3fy5nzm6CqyxhgoQT20tV+S4n2OtRA5H/e33e9wgqC5/pdSC6TtbAX0uAPXEOdh4bB9i2RoBFYvwKq+Bb167A4uysEMSVHRdVTRq1pocg8HEeFLNU1GrhDRbkNkz1J1SIMtksTwCGOE3FLUz9+N/WOJhc8b8d8Z/2+E+PyLcxP5ZVSDAI7pfWSyMpETsZDYaTWF8pIMriZYiyG4/uFr9zHoTtu/NQi9NoclNZkB6vdyPvj/DrYhzAaS381QJgIwmwd+H4Kz/aUQiFsFDnEVhL29WP5Q8ENlFNLDIbTRMIqs9IcgWJV+XlWj5hh4rZTXPcMJpkd044FPb5g4EKvVzfLddsnhAIBq1SPiFhyREgNzDPAfxbR8RYmPfNZiNOUSjkgmupyOMe14ZC9UJFsrxuvPdpAWYaEZcx39XC/6TVaI/jd/rmpJder7+e9Rvr8Xi7J0nBCB+SCUnKdrxCjvhWnsXyRiQccfAzDdt5B/M+n9IsV6vWXEmdKafK/tjn82+VUKcWTqjY4cQHQVoFf80tqHlsAuyvnQxtr0lwrq5FyNmeZUQHjINbnmM0PUJedARV2cdUiytJuG/lQIvjGUNUIbNsDvs/+LOKn+kIukfUSuUwjpyyiUqLCAERsXEwxC54TePfHBc9h0YtXsbOv5383szv5VErlJam+FtIDJaximU9RGBtIdhOMxqM/1dbXzuKf0ued0AgXmrJyf1fVU1NaSAYqGr8vFNh0RQRZlxZUz1SVJDk+zpyrav4axnL6cU6bGT5PgLGR+BN5sSpZF7X87OCJoZEREhq2OpttrFUi+uQTZkT3cTfxSWkCGd3ntS9HXFJldFcUilVuWXFJfW0+t7jxCgW1iwBdBw/c+bnWv4Vt2rLKTn5tVJYsU91Lim1UoXmJuefSd2yqa3eSq22W7fOXZxUN6fur3XMMZlGESxBgslbUtSpoUtJaYS/r+SEKIt9bx7Vubi0trRT8a9dSsvClITXZUe2g4VUSzcIE5tq8WK3x/0tLar99lWxtEIP02m0ZwkjR1i4Xq93JuvriksiJSfG7yh9xRrkHFqy87NDn03ZdACmbARpNrUpdepU3Lm4uLi3wWjQORyOhrRV4W8OL5J4pULZU6NRH6+QK/pp1Gqx+UD4f4TDy+73+X4OhcMLvD7fPFpnGR2FKHxQzFMtPE6Japp/ham62v0szca2kIMN5e+iLWURcXZHzMKt8vt9W2mFzvP5/UtDcXXaOmMIohxVcj9HxNlaoZA/lS9QylBSKhSS+QSDQT8knM2kMJDLZBqgxVVoGSmDL82q7AZUcUnnM84481FWTfg4K2gbldFIUs+cOeNvWzZvWtIisGg9GbRa7eV6re4PrOxxtI90EYm6NmYkTijmwLzvcDpf4MDsSKeStN5uo5EwNpzQOg643OawP8B8PmpHQKmMev3lep3+GrZlqPCRSXVoYwRTOBzeTIC973Q5X2FbKjPmfSrVYQV5+VPimiGSkP3GqtqaSwmutI44JX8sp9X7CeuqTsrnl8qa6otZzyaxarR+x2s12ivTAK8Ap4tjujkQCCzyB4IzvT7vsuYW3EtKSkpHXXHlZz//vHVyVWXlzLr6OmdFxY5N5T3KR54zfORj337z9TUpw0qIdpiMxiuMBuODBNPhon7RK8UESPi0s1atvUdtUf+BJPlugqPFE+w4yOdFxHsCkhI7fkd7gcpoMJxrMhj/zrIGRthpje1pri0E3mEE/IOUaNc5Xa577E7HpEzK1Kg1AwnmvomDJKSP3+8Xnvy0z83VqtVDOAb9E/te5OPz+7ZE4hEoyRJZpVSN5HdHpJM/JY34caxGpR7FjMME2iyn2/Wc2+NpEtEhJOHZ54x8dMmSxe/WVFdNvujiS9e53e5qGku/vvPOm8OnTv3KP2TI0Efl0h2itnCmvWMymt5n5Q4PR8IpASWVwtGlNxQTmO/m5uT8ubl7qSpyWNkjkweZDarkAKxrByklL8jLezrXZP6Svw4UHZWJ0I93bGPUxoMZEViFor/U54FgcGa6qkcASK1SD5bqf9ZtuqTElcksbGva65qNkywsrnBYznqfxrZ+WpRf8B6l7h5vUDMaTfkGg6HXsqWLX+F9nZxOZ/3nn025gFrt+IKCwtPWrlk9VfS5XGKWdcq35H1DFF8pJQ6jTtPdTsNQ4t9Sg0Iz/58Wc86NzcyWnqxGk4B+zprV5Gy2NoJKSzX7gVatuTssIaEybovB8Dd2+Pj0JZZ6QJMyeVHSLMsQoIOl8EA+Kxl7T8lzJNtelMq/lHilAppoL8sdTSx8R3B1b/yuS9eunT0ej4NSys8yIlTTRaedPuwzq9W6wNpQHz1Lnyq1QpnECXKpm79gxw6WGgRWJOwLBL7jg1PYqFWRSNjNbzRareYY6vPLVQrlGXFpteeAGI3/4XPL3R73kqbAUg5izvJkMU9CuThTQpksqQiqiRqN5rLkCSJrVCUB/7eBQPAzcoqVkWhYkIwTT3O0TqO9TKlUnpn8nPib6vRRqujlDpdzarPqRanUc2COaiKJIxErn09bEjOfIql8+HcVx+EnaU6mGpQCMNUsvz4BU+LNxRqFXC4W6DUSZYh+7E9wfVRbXz+MRpltx/btNSeffKqJPFUeDIai7yItKCjIW7165ed2u71ORKyz7wqUiZZZjjnnv/w5uMlAcBCE2CVfGu/xehcmV4AzcJFD7nxNrMfpdLqXEQu9+U3fB/yB2ak4hVqpOl5KzFMNLmqLtMrLyb2boBqdoi3LbXbb3eQQ05OfY1sWiLYY9IZLzUbjy2xrYRNwGY3P8r7ZJPYpF245WL1YVmliX4mpGQqH1lEVVqcNLJWqr1Bte+QTm3greVlTPHNc8hjJZXJYHbbrXB73d4nCSoQ4UbL2oLq90KDX3yri5RKfFb8T2INyTKbH66wNNzsc9l0EdO0xAwaOqq+vm89JYvtxxvSbzj5n+BS73fFDQ31dJVWl+TdVmGM03aBVqS9KHgh5jCS+Vl1Xew4HYmEqKSKea7BZ/2t3OK4RYBKN563raVGNrq6vPY1SYYWEWpUT3QMlZpaHg7aqtaDSajT9Caq/SYGK+U6pa6g/QwpUiW1xOB0f2ez2i/mMZ09iLya5rA9n7Khm1aBW21eWsAuq0f1AFb8iE0ks+FVTdcZ2+PzzpfIhQVJHDZSm0sfuD/iXiNByXr7Gi231UFj8RKHxGMdvKJ+am0wFRH9QI90goosJpMic2TPvP/6EE8f37nP4yXPnzL52+fKlM774/NOTysvLj/jdhRe/uWTJosejDefgFlLS/D1ZjcVA5X+/vqFhD1dAc8nlcn3AGXACf7VyYP4ZDKXezs1O68pO6JU8G1n5LRS721qpApFjNv8dsQ0fyZJqrtVmHUOJkVb4Cy2jOVSNz9LKHZ/YN6K+mlh40cRU5ryQ/FKf+4PBtN8wL+rM/pF81S9BMl/aGFJ0U8qVPZLHkpJyPdvd7JIcAfYrrA2XWHJy5yHpWCdOKBX58k2ckGPXr1+3hh9dPeT4Ex7JycmtJsAu5B0msS3w+++nPbBk8aKvo8Ay6vXXEETF4aQ+CkUiGxvstj+FM5hiYkZTItyWJintC4n3MbMTlqOVmyhI1AeT650Xblplu9VmuyFdUP0GLpfrVRo0tyLmQE0cwMH8vIySeEdTV41cEOhjmkgNsVHQ51ue9iSRyXTkvRL5RBo48ValcE2IyN0mk4r3L2U+Le4rILiq1Cr332movJmsEimARlDNGqkKnQTX0k2bNo7s1r3HcVT7YrG/pqJix0KS+kBMWCmUeq1WNzp5IMTMt9ptD1B0d9gBElqNamjydkoh5kn0F7WGuEfj2/X66yNJO7zjvqPXPD7v+kzzpJGynepzMQd4WBJf0gsfFSReWcfPRUjOERIqfhcnTdrvuhEL6wRp10TpE5foP5FfVaaYrJISjvcvSHsyuV1T9DrdU8KyTNImnflZH/66NO5nxNYtmyW5sFyn1ZxKxB0l4ZxcR/R+2lGgijrxVJpB4aazMeL3+lpF3NkOsaN5uAQofQ6X6/U2VDcV3+uSgjwfwboURpLAzUm6lpcjbWCp1AMhsZ5LqbsglSsohc9LSMq0N0uIsG324SoJV4VcpVR1SWt8Kc4vQNLpdI0kV6xndRSwWIaRs7GfxFeVoXC4VS9y5Aw/ioDtJjFJlpKTbGhtXTkoVSkC/eTSklh9dETCTcR6LM6kXJVSOTQZJHGP+/wU91uSnc1RCRcO76D6yqhPyY0rUixT5aUHLI3mRCmfFblDh8YsqWOzugRNZ/VP5APWVkrBflKzmJ06t02bTWUpt+RFUqijoVL18NEqy8QPR04zSMK687I9S1OUewTLKZRQwcvDsU0raXviCUa/1EuC4zusWq6/WLKRAiyvrR0KLLUQ8xGZBBdq9UkuVEE9mnq6OUn8bdvaRKlemoLz1UkAQkF10U9iicpDCzttFwpBVUqg9Glq2ITXc/JtT1HPwckO9Shn9fmWZsJZxTjQ+CiONNnOQHLv86a1GC+HxCGtQgWyMvUdCSwaDcdFpEnm4lYDS6kypJiBDa1X2dGO7iudbWSrBLBE3H0viZu3ElxpL6pzYIVj1CQhfZdKnfITO6VHeZxUXiJqIdN5D4mgAOHlYDsq0gWWlBhWcvZ32K5fhchfqZRy4nn9GcxqKRGewgWibANYy1jXAU0lUGgnuc4mCedsP/ZfE0AEQ4FVnLBpx5ZJWXdCFLF/ZqWQMqymsr+Ea8JKarEmkzbTIhzE8nsmc7VwKLQjGAhuSRdYLolKqtk5XToMWApFmTiuSEJSbgqEQttbmy8lgk/Kr8bZ37W1eep1+guoTnKa+oWC88Q2NolH+kiT4XBG72nWqNVDJCZKMBgOLk1B3LvQGDosuZ6iT6kFdmXgOxOBA7eK3esS2mRGKJzemV0CWCtSzNQTO5Bf9YtvRE0m7isoCVodMSokiJT1plaqhrRKXSuVas7eW8ISfkVyjckpJKSuqaQhz/P6rBlISTMnXhPHaCgS+cXvD2xOwS+PlsUiRpNdE0vFLu50y9bpdKcwr99LtcHj972fNkBp/U2TWhtih16uVCgyUiEiH4Nef4K8hT145FeDU5i4bTqCMWrOJ3mXxeCo1OphtH6LMs0vx2S6h206SkLl/kwO+nUqwSklNbVaTXH6UlJ7EfuwJFkNcuLNk5LKURVM4p7CNZF2n2o12s45JvN/WYZSYmwWeTyeWWkDy+X2fEBTVMq6OdpkNN6SCajycnPH5uVaZhfmFXwkdlc3I7FOkLLeaDUtawuw+Pw6imspjpZv0hv+L5O8OEEu0Wl0D0lFCXi83scpCdwp+mGnFPfjwI8Q0ZdpSPNCg97wYFjCBeTzeSelCOwT43W8RLmkRaFlaYLqcI7fV+KMNAksiMNeHkw3lDr6jD/g3xgMBj6Xllr6x81G4/npgMqSk3uXTqt7kYULZn5JQa5lAdF/kwi2S+ICuUpl0/gi6u4Kr8+3pC3AYp0DBNeEZIkZXzS+XYRap9OWHLN5TK45512qQGUTdR0OzbY7HG+mel6E+8QPp0vmlScRrGNa8O3ls9wPWU55E64UDi9xut0/SBtDCos4HkEi9msLJevq5g0phYFljs23WGay146W9Gl6vROcLte3GdEIkREfejI/V305s9QnDYjOZDRN4Sx6ive8ItbNkqw7MWDHGw3G+wiYCxqdkPHKFZqNplfZ4G51DfXjEzqvlxzyTuGmGqOa+RzLh+UtOSsDgWBtqjMUXG7XWzqt5mbeeFRSWxSszzskxUeyLS+zLbuSO5DqfyClxR2s41VSDlW2qtZqt90YaoYH+gMBTtTgXLb79MRBisZx6Q2vCl7ucrnfYh6hBIkgI+jOMhmMT7Ee/aUG1+V2PyQmTgqi30tE4SbXORIO1xkMhuNYcaWEY7eEAuA4rUrzO7lC3ieVJGQes60O+13hSGYO5t+mNsXgnQat/l+hiPQalHAGcjbO4ywQM0AsTHdTqZQDiXjhO5FJheDywc31VuvvPF7PT7t5i/lP7MCXJSoakcdihFuUKG6355k6a/3dqe4xGgynchZ+x45WpWhLFdsym21ZC/HeJXayQiEfrFZG19nUUp3MSeSpt9kuJHCntahGdfqzLDk508JS8VJUpeQrS6hKBV8Rh5h0JgiHqhSKYyXvl0dV78v11oZbUrlTOGFuMZtML0pMhmb7tLkNJVH3QiQ8p66h4SL2VW3G/r9E6ZNnyfs30T8u1fKHTELFpL4v8lO91XYhQbWHr6cgL/9NlnF1a8OORd6UGhxg92fNE2/zWAL4lVQzTcp6TDlrI5FaAuoPdqdzajr1Fnwxz2J5XqfR3BZOsb0MafRlPIZsak193UWUginN/MK8/LepVa5qSyh3Mpgped9iP99GULUqukW+m+OEo3FU1KcPsUHhVB2feKWqFDvh89qGhjOTQRVf/xrYxna7RMx5SzfZHPZXHS7H1SzSlU5bIimkBVXWrAab9VSbwzE13YET1pkIfaYh8a7EfpXYcYgtlU3JFggG3q6tr7+sOVApYsfoDGgrqGIbSeSCly13OJ2X1dTVXtNaUO0hsfZQJXrDWdTNj5A3DWkORImVksU6a7PT435CnK4sJfV0Wm3vAkveBjGLZa1rfTScp6q25qh0fTMscxCl1xNKhfLMCNJtS1QNbKIKeo5E/XWCy9/amU8VdS9Vo7BIc9Mtm+VtdLMfKSHfaOkZjVpzeFFBwTrR3609aInjUUvBMp+CYBL53xSW722r1JM10ykKdsgIrUbze86IE/l31+gRjntG5bE+4Wpei6iaPiYh/lzs5Ejp+FOp+pgMhnHsq2ArcaUMhcILKY3eyXSA2ZYz2ZYxbMsZ/LssegL0nm0Rx0dWEbgLaVl+QtXHtgRtaIekVqnLyfuuJwW4gGX3FisbSWVHIuFIrYjypBX3CSenOAgurbJpPPVh28YlnN2a7riLuLDtLG9jIBRcQ6lY016qtFlgJZukarWqh0wmjnmMWBBbuK7j4yLO52eSUWt7VqojE9tiYlt6xtuSF9dM9WzLzkDAv5nqy9ZRbSGoWLTYR6koZ7H5cSrSQKDtoqW7hX1ZF8GB0Y/ZlE3ZlE3ZlE3ZlE3ZtA+47KHeAcdAk/97GC88Hrr+QUQqdyHUZHG5B1S60TCdeBy0Zw+BtsQP2Kuw54Fs3XnPH5FzbJjW+w7s3onTD5qCa2E+ugFhe038/YOi06+BuVd/aHqshG/XGdB1/R2MRw2EpmwwtOLqciI/00AW+RVBO58/lvfqV8NXn0jt88j9z4R+4AgYhrNefZSAh/VqSAwvPRxq08PIu+Q7eNZIuYovh7H/ydDmr4G/ptGsPAJqw5UwnXc8tEMtUNg2o3V7EA7ZNIZgqUGPHREcRjuwl3hncs2tyDkn8Z6/Iu/8X9F9a+ye2OVET+drKPo/ZYL7nIN7ZAS9I39H3h5RFDch50rx+bUJr/sVL0Xaim4fb0C3aFTJG+j0T3GPHz0jVpRHf4q/X0XhY+J73mvbiG6TlAlGPEF89Dp0neWL3hurl5u/f4GSiZwsv22uPRJqrQc9f/0viu5TSTgB5qPzpjr0mJ0X95WPhL63eH1wY54O9PQ8ivyrM5VAykMVVAVQyMbDwgGF8a+oG85Z6X4AeS8dBpXYXPKtGIJ/IP+ivyD3k0qE1t2CmjGUBstzIC+5DqY/3QjzE3y25E7U3OFGBAHxlgH+501yF/jjryVKfv+gnZ+J19kq+P9LsL7+LVyzh0J39A0w//1F2J5cBO+8DQisJ5iUvFeW6KQaBVPf51Awk2Wq3oTjz9PgnkHpph8N4+XnwDCOwOp+Fnaetx5+j5Cg9Qh5L4fpMf7u+BNqXgwk1MXJvG28wrsnwvgiKI68B7VX7UBow8OwPEfJ1T+HcrYeoaw0aimVQ6msRY9tK9F1ZUGcEegh+22isTPzhATbhu7rqAItic/mcnZ/iZIJQsrdBPNp4jOqpCPFG+kJ1nsS76WkGiNmPqXjHhJrBbp8tBhdapUJZV4B00ni3kuxO1SJ92p4r3UJurwvZIqBUpJSZrYdPV03I6f/nlJChgko+pOox8sovENMjj5Qq3eg+1rxsnRKrsjrKLoqUfp8h9KNlFCzcuMS63uUTqtEjxr2SbRe4u2vmlb49A/Zl41XIBScBc9bfaE+mp07815YLsuH4jcaQk5zlhnygudhfZDSY49dPlZKm3tQ90Adgv7zQDoSlUltd2zG33Aqfmqlvg/HOGGfwdCc9CZsL78M2x67m8ULy+9D3aub4N9wDvTXEhCyECJhqkD9FgRm8fryapjefhVFV6hTgGUxfO8UsN0E2LJ/oeA69onB14q2HbLAEp11J2of+QjO+4uh7P048idPQ+n8y2CMRlAOh+5wIfhJuCUjMDciQKIf3FgIZaPU2Csu80h8W38dQnOkvq9FKLIVgcUc2MMQi68LUxKrFsJbcw2qRu1ke66H+f3rYB6Z+FwjzB5A3Tv/QMMtAlB3InfiXHReSYI/RJYFVvqJFpf/clQ+ejJ2EFgN48qgPI7ke4KJ3cKZ26CIdpBMcks5VYTKwJmNWGxacynhQOkmAkjWCkngkcXq1UnqeyGJWLeC+H3BOBgjRsj1S+BzXYWqERUIrngM+VMugXGYB7Ed0rLfpB7wMOpfPhUVRz6BhtHkY0X/RMF7nHzGLLDSSDTpLQ8ib1R3qLqRuDvGo+7Fr+Ge3JngMkKmXgTfj0K9XQC95Ht3bkHOeV2hKl4L37fxgZHF0bKH5KIaisQlpDqR0AujQZ7wQtF0kwuRtTQW7GdDf41WApfnw1B+LLSnrUdgLo0Dn3y3SylaDtV/9RhUne9BuOIVFH7eF5oerJtPhKZaINfeA8slw6HvR6nno1qdNBeeZ6hSeyoQfStaFlgtpeOhOeJvKJj0DAruyGc3lJDM94Gqhxg0gkE2B55VP8L7ETnUWFpgt/eGOhqNypmPPyP3jHuoJmwIbX8BtjdjwJJFR45qR5EHhZyqRMGBl3GAVgogjYHxWlpb0f6+EqaB3aAaxs/nIoNzwARCllOSfgrXY0OgHToRRRPIuSyyGC/DMOiOuA+WD2lpqlmvxwTnkkuEjxJcO65A1dksf1ce5CZOhqCwFIugLHoSBR+Rbz4iSLswaijFj2R+IVks0jabWkqlUKhXoevXQVpQq9H1R/6+Khyzpm6R/3aPMmc2Ok8Vlhqtqi1fo/RTWpGLvbSuqtHjF3KV37axUYL0FZ9XoLuVVta6OvTY8EeYTxffvYrCp0Qea9F19VSUfuFCub8ePWpHQL+HVXcDzMOFpUmCfUWiVbgOXYOs4yeNfiyqatlHKH5G5FlPy5VE+4tF6DxdWH0uWosPIW+MbLezU+1Hz/o30anJ0ZinEIisb+1mWoVC/YtJMxnF/xF+tJXosoD1nS9+J4Cf1mWotQ9Zz7sDkRBn7lfsMBkHbwAllW0i7ONJXCc2WkEOhH3fwP0+u3QLPxEnAfchJ3F8B/dLd6D25qkJb5unlFJSqhl3ILi1DuFqG8KVM+Gd/hP8u76F5ztaklspFXszj25bEPziTtTdOA3utXuCXanuCaXhK7i/oXreGVMpMtlx0ObTip33GVxLI3FVSrU9bRsC85mfQQt5Xz+gnA/vpDtQc+M7cPzYmCd5oGwgNHmL4V08G96FSRyzlhJwzqnQdZkE55fC2mWbpnWC0s08+1Ptyr6E+ym29R+ZWob/L8AAw015AciTw4kAAAAASUVORK5CYII=" alt="Medical AI Logo" class="header-logo">
           <div class="header-text">
               <h1 class="header-title">
                   Medical Support Authorization AI
               </h1>
               <p class="header-subtitle">
                   Instant, Evidence-Based Procedure Authorization Decisions
               </p>
               <div class="header-accent"></div>
           </div>
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
        st.markdown("### Quick Templates")
        
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
    """Render the patient input section with premium styling"""
    
    # Add premium CSS styling
    st.markdown("""
    <style>
    /* Premium Input Section Styling */
    .input-section-title {
        color: #212529 !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin: 0 0 1rem 0 !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid #dc3545 !important;
        display: inline-block !important;
    }
    
    /* Fix procedure boxes and text visibility */
    .element-container:has([data-testid="metric-container"]) {
        margin: 0.5rem 0 !important;
    }

    [data-testid="metric-container"] {
        background: white !important;
        border: 2px solid #e9ecef !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
        min-height: 80px !important;
        height: auto !important;
        max-height: 120px !important;
    }

    [data-testid="metric-container"]:nth-child(1) {
        border-color: #6c757d !important;
    }

    [data-testid="metric-container"]:nth-child(2) {
        border-color: #28a745 !important;
    }

    [data-testid="metric-container"]:nth-child(3) {
        border-color: #dc3545 !important;
    }

    [data-testid="metric-container"]:nth-child(4) {
        border-color: #ffc107 !important;
    }

    /* Fix text color in metrics - more specific selectors */
    [data-testid="metric-container"] * {
        color: #212529 !important;
    }

    [data-testid="metric-container"] .metric-value {
        color: #212529 !important;
        font-weight: 700 !important;
    }

    [data-testid="metric-container"] .metric-label {
        color: #6c757d !important;
        font-weight: 500 !important;
    }

    /* Make procedure list text visible - stronger selectors */
    .procedure-details * {
        color: #212529 !important;
        background: transparent !important;
    }
    
    /* Fix white text in procedure listings */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #212529 !important;
    }
    
    /* Force all text to be visible */
    .main * {
        color: #212529 !important;
    }
    
    /* Specific fix for procedure items */
    strong {
        color: #212529 !important;
    }
    
    /* Override any white text */
    [style*="color: white"], [style*="color: #ffffff"] {
        color: #212529 !important;
    }
    
    /* Enhanced Text Area */
    .stTextArea > div > div > textarea {
        background: #ffffff !important;
        border: 2px solid #e9ecef !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', monospace !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.05) !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #dc3545 !important;
        box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1) !important;
        outline: none !important;
    }
    
    /* Premium Validation Feedback */
    .validation-feedback {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%) !important;
        border: 1px solid #ffeaa7 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
        border-left: 4px solid #f39c12 !important;
    }
    
    .validation-success {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
        border: 1px solid #c3e6cb !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
        color: #155724 !important;
        font-weight: 500 !important;
        text-align: center !important;
        border-left: 4px solid #28a745 !important;
        box-shadow: 0 2px 8px rgba(40, 167, 69, 0.1) !important;
    }
    
    /* Premium Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3) !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(220, 53, 69, 0.4) !important;
        background: linear-gradient(135deg, #c82333 0%, #a71e2a 100%) !important;
    }
    
    .stButton > button:disabled {
        background: #6c757d !important;
        color: #ffffff !important;
        cursor: not-allowed !important;
        transform: none !important;
        box-shadow: none !important;
        opacity: 0.6 !important;
    }
    
    /* Secondary Button for Clear */
    .stButton:last-child > button {
        background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%) !important;
        box-shadow: 0 4px 12px rgba(108, 117, 125, 0.3) !important;
    }
    
    .stButton:last-child > button:hover {
        background: linear-gradient(135deg, #5a6268 0%, #495057 100%) !important;
        box-shadow: 0 6px 20px rgba(108, 117, 125, 0.4) !important;
    }
    
    /* Input Help Text Styling */
    .stTextArea > div > div > div > div {
        color: #6c757d !important;
        font-size: 0.875rem !important;
        font-style: italic !important;
    }
    
    /* Label Styling */
    .stTextArea > label {
        color: #495057 !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Placeholder Enhancement */
    .stTextArea > div > div > textarea::placeholder {
        color: #6c757d !important;
        font-style: italic !important;
        opacity: 0.8 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Section title with styling
    st.markdown('<h3 class="input-section-title">Patient Case History</h3>', unsafe_allow_html=True)
    
    # Initialize persistent template in session state
    if 'patient_input_data' not in st.session_state:
        st.session_state.patient_input_data = """Age: 
Complaint: 
History: 
Procedures Requested: """
    
    # Check if there's a justification update flag
    if st.session_state.get('justification_added', False):
        # Use the updated data that includes justifications
        display_value = st.session_state.get('updated_case_data', st.session_state.patient_input_data)
        # Clear the flag
        st.session_state.justification_added = False
    elif st.session_state.get('example_case'):
        # Load example if selected
        display_value = st.session_state.example_case
    else:
        # Use persistent data
        display_value = st.session_state.patient_input_data
    
    patient_data = st.text_area(
        "Enter patient case details:",
        value=display_value,
        height=350,
        placeholder="""Age: 65 (or "60s", "elderly", "middle-aged")

Procedures Requested:
- Heart monitor
- Blood tests  
- MRI scan

Additional Case Details:
Complaint: Heart problems for 2 weeks
History: High blood pressure, diabetes
Family History: Father had heart attack
Symptoms: Chest pain, shortness of breath
Physical Exam: Blood pressure 150/90
Previous Tests: EKG showed irregularities""",
        help="Fill in the pre-written fields above. Age and procedures can be approximate - the AI will understand context and medical terminology!",
        key="patient_input_persistent"
    )
    
    # Update session state with current input (only if not using example)
    if not st.session_state.get('example_case'):
        st.session_state.patient_input_data = patient_data
    
    # Show validation feedback in real-time
    if patient_data:
        feedback = get_validation_feedback(patient_data)
        if feedback:
            st.markdown('<div class="validation-feedback">', unsafe_allow_html=True)
            st.write("**Suggestions to improve your case:**")
            for item in feedback:
                st.write(f"• {item}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="validation-success">Case ready for AI analysis!</div>', unsafe_allow_html=True)
    
    # Analysis button - more accessible now
    can_analyze = len(patient_data.strip()) >= 10  # More lenient
    
    analyze_button = st.button(
        "Analyze Case",
        type="primary",
        use_container_width=True,
        disabled=not can_analyze,
        help="Analyze this medical case for instant authorization decision"
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
        
        # REMOVED: render_diagnosis_display(result) - this line is deleted
        
        # Analysis timestamp
        if 'analysis_time' in st.session_state:
            st.caption(f" Analysis completed: {st.session_state.analysis_time}")
        
        # Technical details (collapsible)
        with st.expander(" Structured Summary"):
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
                <div class="metric-label">Total </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Total Summary ", key="btn_total", use_container_width=True):
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
                <div class="metric-label"> Pending</div>
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
            title = " Pending Procedures"
        
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
        card_class, status_text, status_color = "pending", " PENDING", COLORS['pending']
    
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
                submit_justify = st.form_submit_button(" Re-analyze", type="primary")
            with col2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state[f"show_justify_{justify_key}"] = False
                    st.rerun()
            
            if submit_justify and justification_text.strip():
                handle_justification_submission(procedure_data, original_case, justification_text, justify_key, index, procedure_name)

def handle_justification_submission(procedure_data, original_case, justification_text, justify_key, index, procedure_name):
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
        
        # STAKEHOLDER REQUIREMENT: Add justification to original input textbox (SIMPLIFIED)
        if justification_text.strip():
            # Create simple justification entry
            timestamp = datetime.now().strftime("%m/%d %H:%M")
            status_emoji = "✅" if new_decision == "APPROVED" else "❌" if new_decision == "DENIED" else "⏳"
            
            justification_entry = f"""

JUSTIFICATION {timestamp}: {procedure_name} → {status_emoji} {new_decision}
{justification_text.strip()}"""
            
            # Get the CURRENT text that's actually displayed in the text area
            # Clear any example case first
            if 'example_case' in st.session_state:
                del st.session_state['example_case']
            
            # Get the CURRENT text that's actually displayed in the text area
            current_displayed_text = st.session_state.get('patient_input_persistent', 
                                                         st.session_state.get('patient_input_data', ''))
            
            # Add justification to the current displayed text
            updated_data = current_displayed_text + justification_entry
            
            # Store the updated data separately and set a flag
            st.session_state.updated_case_data = updated_data
            st.session_state.justification_added = True
            st.session_state.patient_input_data = updated_data
            
            # Also add to last_case for exports
            if 'last_case' in st.session_state:
                st.session_state.last_case = st.session_state.last_case + justification_entry
            
            # Store justification history for exports
            if 'justification_history' not in st.session_state:
                st.session_state.justification_history = []
            
            st.session_state.justification_history.append({
                'timestamp': timestamp,
                'procedure_name': procedure_name,
                'justification_text': justification_text,
                'original_decision': procedure_data.get('decision'),
                'new_decision': new_decision,
                'ai_assessment': justify_result.get('justification_assessment', ''),
                'decision_changed': decision_changed
            })
        
        # Update ONLY this specific procedure
        if decision_changed and new_decision == "APPROVED":
            procedure_data['decision'] = new_decision
            procedure_data['reasoning'] = justify_result.get('reasoning', procedure_data['reasoning'])
            procedure_data['confidence'] = justify_result.get('confidence', procedure_data['confidence'])
            
            st.success(" **Decision Changed to APPROVED!**")
            st.success("✅ **Justification has been added to your original case input above.**")
            
        elif decision_changed:
            if new_decision == "DENIED":
                st.error("❌ **Still DENIED** - Additional justification not sufficient")
            else:
                st.warning(" **Still PENDING** - More information needed")
            st.info(" **Justification has been added to your original case input above.**")
        else:
            st.info(" **Decision Unchanged** - Original decision stands")
            st.info(" **Justification has been added to your original case input above.**")
        
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
        if st.button("📖 Export Text", use_container_width=True):
            # Create a comprehensive text summary that can be downloaded
            pdf_content = generate_text_summary(result)
            st.download_button(
                label="📥 Download Complete Receipt",
                data=pdf_content,
                file_name=f"medical_authorization_receipt_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with col2:
        if st.button("📊 Export JSON", use_container_width=True):
            # COMPREHENSIVE: Include ALL AI data, justifications, and metadata
            export_data = dict(result)
            
            # Add all justification data
            if 'justification_history' in st.session_state:
                export_data['justification_history'] = st.session_state.justification_history
            
            # Add complete case data
            if 'last_case' in st.session_state:
                export_data['complete_case_data_with_justifications'] = st.session_state.last_case
            
            # Add session metadata
            export_data['export_metadata'] = {
                'exported_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ai_model': 'gemini-1.5-flash',
                'analysis_session_id': id(st.session_state),
                'total_justifications_submitted': len(st.session_state.get('justification_history', [])),
                'export_type': 'comprehensive_ai_receipt'
            }
            
            # Add all available AI explanations and reasoning
            if result.get('multiple_procedures'):
                for proc in export_data.get('procedures', []):
                    # Ensure all AI reasoning fields are included
                    proc.setdefault('reasoning', 'No AI reasoning provided')
                    proc.setdefault('clinical_indication', 'Not specified by AI')
                    proc.setdefault('urgency', 'Not assessed by AI')
                    proc.setdefault('estimated_cost', 'Not estimated by AI')
                    proc.setdefault('missing_info', [])
                    proc.setdefault('alternatives', [])
                    proc.setdefault('guidelines_referenced', [])
            
            json_data = json.dumps(export_data, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Download Complete AI Data",
                data=json_data,
                file_name=f"ai_authorization_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("📋 Copy Brief", use_container_width=True):
            # Generate comprehensive summary text for copying
            summary_text = generate_text_summary(result)
            
            # Display the summary in a text area that users can copy from
            st.text_area(
                "📋 Copy this comprehensive receipt:",
                value=summary_text,
                height=200,
                help="Select all text (Ctrl+A) and copy (Ctrl+C). This includes all AI explanations and justifications."
            )

def generate_text_summary(result):
    """Generate a comprehensive text summary of ALL authorization results with full AI explanations"""
    summary = []
    summary.append("🏥 COMPREHENSIVE MEDICAL AUTHORIZATION RECEIPT")
    summary.append("=" * 60)
    summary.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary.append("")
    
    # Add original case with justifications if available
    if 'last_case' in st.session_state:
        summary.append("COMPLETE CASE DATA WITH JUSTIFICATIONS:")
        summary.append("-" * 45)
        summary.append(st.session_state.last_case)
        summary.append("")
    
    # Add DETAILED authorization decisions with ALL AI explanations
    if result.get('multiple_procedures'):
        # Multiple procedures - FULL DETAILS
        procedures = result.get('procedures', [])
        summary.append("DETAILED AUTHORIZATION DECISIONS:")
        summary.append("-" * 35)
        
        approved_count = 0
        denied_count = 0
        pending_count = 0
        
        for i, proc in enumerate(procedures, 1):
            decision = proc.get('decision', 'UNKNOWN')
            procedure_name = proc.get('procedure_name', proc.get('procedure_type', 'Unknown Procedure'))
            reasoning = proc.get('reasoning', 'No reasoning provided')
            confidence = proc.get('confidence', 0)
            urgency = proc.get('urgency', 'Not specified')
            cost_estimate = proc.get('estimated_cost', 'Not specified')
            clinical_indication = proc.get('clinical_indication', 'Not specified')
            
            # Count decisions
            if decision == 'APPROVED':
                approved_count += 1
                status_icon = "✅"
            elif decision == 'DENIED':
                denied_count += 1
                status_icon = "❌"
            else:
                pending_count += 1
                status_icon = "⏳"
            
            summary.append(f"{i}. {status_icon} {decision}: {procedure_name}")
            summary.append(f"   AI Confidence Level: {confidence}%")
            summary.append(f"   Clinical Indication: {clinical_indication}")
            summary.append(f"   Medical Urgency: {urgency}")
            summary.append(f"   Cost Classification: {cost_estimate}")
            summary.append(f"   AI Medical Reasoning:")
            summary.append(f"   {reasoning}")
            
            # Add missing info if procedure was denied/pending
            missing_info = proc.get('missing_info', [])
            if missing_info:
                summary.append(f"   Additional Info Needed: {', '.join(missing_info)}")
            
            # Add alternatives if provided
            alternatives = proc.get('alternatives', [])
            if alternatives:
                summary.append(f"   Alternative Treatments: {', '.join(alternatives)}")
            
            # Add guidelines referenced
            guidelines = proc.get('guidelines_referenced', [])
            if guidelines:
                summary.append(f"   Medical Guidelines Referenced: {', '.join(guidelines)}")
            
            summary.append("")
        
        # Add summary stats
        summary.append("AUTHORIZATION SUMMARY STATISTICS:")
        summary.append("-" * 32)
        summary.append(f" Total Procedures Reviewed: {len(procedures)}")
        summary.append(f" Approved Procedures: {approved_count}")
        summary.append(f" Denied Procedures: {denied_count}")
        summary.append(f" Pending Additional Info: {pending_count}")
        summary.append("")
        
        # Overall AI assessment
        if result.get('overall_summary'):
            summary.append("AI OVERALL CASE ASSESSMENT:")
            summary.append("-" * 28)
            summary.append(result['overall_summary'])
            summary.append("")
    
    else:
        # Single procedure - FULL DETAILS
        decision = result.get('decision', 'UNKNOWN')
        procedure_name = result.get('procedure_name', result.get('procedure_type', 'Unknown Procedure'))
        reasoning = result.get('reasoning', 'No reasoning provided')
        confidence = result.get('confidence', 0)
        urgency = result.get('urgency', 'Not specified')
        cost_estimate = result.get('estimated_cost', 'Not specified')
        clinical_indication = result.get('clinical_indication', 'Not specified')
        
        if decision == 'APPROVED':
            status_icon = "✅"
        elif decision == 'DENIED':
            status_icon = "❌"
        else:
            status_icon = "⏳"
        
        summary.append("DETAILED AUTHORIZATION DECISION:")
        summary.append("-" * 32)
        summary.append(f"{status_icon} FINAL DECISION: {decision}")
        summary.append(f" Procedure: {procedure_name}")
        summary.append(f" AI Confidence Level: {confidence}%")
        summary.append(f" Clinical Indication: {clinical_indication}")
        summary.append(f" Medical Urgency: {urgency}")
        summary.append(f" Cost Classification: {cost_estimate}")
        summary.append("")
        summary.append(" AI MEDICAL REASONING:")
        summary.append(reasoning)
        summary.append("")
        
        # Add additional details
        missing_info = result.get('missing_info', [])
        if missing_info:
            summary.append("ℹ  ADDITIONAL INFORMATION NEEDED:")
            for info in missing_info:
                summary.append(f"   • {info}")
            summary.append("")
        
        alternatives = result.get('alternatives', [])
        if alternatives:
            summary.append(" ALTERNATIVE TREATMENTS CONSIDERED:")
            for alt in alternatives:
                summary.append(f"   • {alt}")
            summary.append("")
        
        guidelines = result.get('guidelines_referenced', [])
        if guidelines:
            summary.append(" MEDICAL GUIDELINES REFERENCED:")
            for guideline in guidelines:
                summary.append(f"   • {guideline}")
            summary.append("")
        
        risk_factors = result.get('risk_factors', [])
        if risk_factors:
            summary.append("⚠️  PATIENT RISK FACTORS IDENTIFIED:")
            for risk in risk_factors:
                summary.append(f"   • {risk}")
            summary.append("")
    
    # Add COMPLETE justification appeals history with AI assessments
    if 'justification_history' in st.session_state and st.session_state.justification_history:
        summary.append("COMPLETE JUSTIFICATION APPEALS HISTORY:")
        summary.append("-" * 42)
        for i, justification in enumerate(st.session_state.justification_history, 1):
            summary.append(f"Appeal #{i}: {justification['procedure_name']}")
            summary.append(f"    Submitted: {justification['timestamp']}")
            summary.append(f"    Original Decision: {justification['original_decision']}")
            summary.append(f"    Updated Decision: {justification['new_decision']}")
            summary.append(f"    Decision Changed: {'Yes' if justification['decision_changed'] else 'No'}")
            summary.append(f"    Provider Justification:")
            summary.append(f"      {justification['justification_text']}")
            summary.append(f"    AI Re-Assessment:")
            summary.append(f"      {justification['ai_assessment']}")
            summary.append("")
    
    # Add COMPLETE differential diagnoses with AI confidence levels
    diagnoses = result.get('differential_diagnosis', [])
    if diagnoses:
        summary.append("AI DIFFERENTIAL DIAGNOSIS ANALYSIS:")
        summary.append("-" * 35)
        for i, diag in enumerate(diagnoses, 1):
            if diag and diag.get('diagnosis'):
                name = diag.get('diagnosis', 'Unknown condition')
                icd10 = diag.get('icd10', 'No code available')
                confidence = diag.get('confidence', 0)
                summary.append(f"{i}.  Condition: {name}")
                summary.append(f"    ICD-10 Code: {icd10}")
                summary.append(f"    AI Likelihood Assessment: {confidence}%")
                summary.append("")
    
    # Add all other AI-generated sections
    if result.get('recommendations'):
        summary.append("AI CLINICAL RECOMMENDATIONS:")
        summary.append("-" * 27)
        summary.append(result.get('recommendations', ''))
        summary.append("")
    
    if result.get('next_steps'):
        summary.append("AI SUGGESTED NEXT STEPS:")
        summary.append("-" * 23)
        summary.append(result.get('next_steps', ''))
        summary.append("")
    
    # Add technical AI analysis details
    summary.append("AI SYSTEM ANALYSIS METADATA:")
    summary.append("-" * 30)
    summary.append(f" AI Model: Gemini-1.5-Flash")
    summary.append(f" Analysis Timestamp: {result.get('analyzed_at', 'Not recorded')}")
    summary.append(f" Response Format: {'Multiple Procedures' if result.get('multiple_procedures') else 'Single Procedure'}")
    summary.append("")
    
    # Add comprehensive disclaimer
    summary.append("IMPORTANT MEDICAL & LEGAL DISCLAIMERS:")
    summary.append("-" * 40)
    summary.append("  This AI-generated authorization analysis is for informational")
    summary.append("    and workflow assistance purposes only.")
    summary.append(" All final authorization decisions must be reviewed and")
    summary.append("    approved by qualified healthcare professionals.")
    summary.append(" This analysis does not constitute medical advice.")
    summary.append(" Insurance authorization specialists should validate")
    summary.append("    all decisions according to policy guidelines.")
    summary.append(" This document contains protected health information (PHI).")
    
    return "\n".join(summary)

# Optional: Add a function to view saved cases
def render_saved_cases():
    """Display saved case history"""
    if 'saved_cases' in st.session_state and st.session_state.saved_cases:
        st.markdown("####  Saved Cases")
        
        for i, case in enumerate(reversed(st.session_state.saved_cases), 1):
            with st.expander(f"Case {len(st.session_state.saved_cases) - i + 1} - {case['timestamp']}"):
                st.write("**Diagnoses:**")
                diagnoses = case['result'].get('differential_diagnosis', [])
                for j, diag in enumerate(diagnoses[:3], 1):  # Show top 3
                    if diag and diag.get('diagnosis'):
                        st.write(f"{j}. {diag.get('diagnosis')} - Likelihood: {diag.get('confidence', 0)}%")
                
                if st.button(f" Delete Case {len(st.session_state.saved_cases) - i + 1}", key=f"delete_{i}"):
                    st.session_state.saved_cases.remove(case)
                    st.rerun()
    else:
        st.info("No saved cases yet. Save some diagnosis results to see them here!")



def render_diagnosis_display(result):
    """Render improved diagnosis display"""
    diagnoses = result.get('differential_diagnosis', [])
    
    if diagnoses:
        # Filter out empty diagnoses first
        valid_diagnoses = [diag for diag in diagnoses if diag and diag.get('diagnosis') and str(diag.get('diagnosis')).strip()]
        
        if valid_diagnoses:
            st.markdown("---")
            st.markdown("####   Differential Diagnoses")
            
            # Add the CSS inline to ensure it's applied
            st.markdown("""
            <style>
            .diagnosis-container {
                background-color: white !important;
                padding: 0px !important;
                margin: 0px !important;
                border-radius: 10px;
            }
            
            .diagnosis-item {
                display: flex !important;
                justify-content: space-between !important;
                align-items: center !important;
                background-color: #f8f9fa !important;
                border: 1px solid #e9ecef !important;
                border-radius: 8px !important;
                padding: 15px !important;
                margin: 8px 0 !important;
                min-height: 60px !important;
            }
            
            .diagnosis-info {
                flex-grow: 1 !important;
            }
            
            .diagnosis-name {
                font-size: 16px !important;
                font-weight: bold !important;
                color: #333 !important;
                margin: 0 0 5px 0 !important;
                line-height: 1.2 !important;
            }
            
            .diagnosis-code {
                font-size: 14px !important;
                color: #666 !important;
                margin: 0 !important;
                line-height: 1.2 !important;
            }
            
           .confidence-badge {
                background-color: #e0ebf8 !important;
                color: black !important;
                padding: 8px 12px !important;
                border-radius: 20px !important;
                font-weight: bold !important;
                font-size: 14px !important;
                min-width: 80px !important;
                text-align: center !important;
                border: 1.5px solid #1f2937 !important;
                box-shadow: 0 2px 8px rgba(31, 41, 55, 0.15) !important;
}
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="diagnosis-container">', unsafe_allow_html=True)
            
            for i, diag in enumerate(valid_diagnoses, 1):
                name = diag.get('diagnosis', 'Unknown condition')
                icd10 = diag.get('icd10', 'No code')
                confidence = diag.get('confidence', 0)
                
                st.markdown(f"""
                <div class="diagnosis-item">
                    <div class="diagnosis-info">
                        <div class="diagnosis-name">{i}. {name}</div>
                        <div class="diagnosis-code">ICD-10: {icd10}</div>
                    </div>
                    <div class="confidence-badge">Likelihood: {confidence}%</div>
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