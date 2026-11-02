
import streamlit as st

st.set_page_config(
    page_title="MBTI 진로 탐색",
    page_icon="🎯",
    layout="wide"
)

# -----------------------------
# 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F7F8FC;
}
h1 {
    color: #5865C3;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #777777;
    font-size: 18px;
}
.job {
    background-color: white;
    padding: 22px;
    border-radius: 15px;
    border: 1px solid #E5E7F2;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# MBTI 진로 데이터
# -----------------------------
careers = {
    "ISTJ": [
        {
            "name": "회계사",
            "major": "경영학과, 회계학과",
            "personality": "꼼꼼하고 책임감이 강하며 숫자와 자료를 정확하게 다루는 성향",
            "salary": "약 5,000~8,000만 원"
        },
        {
            "name": "품질관리 전문가",
            "major": "산업공학과, 화학공학과",
            "personality": "체계적이고 세부적인 부분까지 확인하는 것을 좋아하는 성향",
            "salary": "약 3,500~5,500만 원"
        }
    ],
    "ISFJ": [
        {
            "name": "간호사",
            "major": "간호학과",
            "personality": "배려심이 많고 책임감 있게 다른 사람을 돌보는 성향",
            "salary": "약 3,500~5,000만 원"
        },
        {
            "name": "초등학교 교사",
            "major": "초등교육과",
            "personality": "인내심이 있고 친절하며 다른 사람을 가르치는 것을 좋아하는 성향",
            "salary": "약 4,000~6,000만 원"
        }
    ],
    "INFJ": [
        {
            "name": "심리상담사",
            "major": "심리학과, 상담심리학과",
            "personality": "공감 능력이 뛰어나고 다른 사람의 고민을 이해하는 성향",
            "salary": "약 3,000~4,500만 원"
        },
        {
            "name": "사회복지사",
            "major": "사회복지학과",
            "personality": "따뜻하고 배려심이 있으며 사회에 도움을 주고 싶은 성향",
            "salary": "약 3,000~4,000만 원"
        }
    ],
    "INTJ": [
        {
            "name": "데이터 분석가",
            "major": "통계학과, 데이터사이언스학과",
            "personality": "논리적이고 분석적이며 문제 해결을 즐기는 성향",
            "salary": "약 4,000~6,000만 원"
        },
        {
            "name": "소프트웨어 개발자",
            "major": "컴퓨터공학과, 소프트웨어학과",
            "personality": "독립적으로 생각하고 새로운 기술을 배우는 것을 좋아하는 성향",
            "salary": "약 4,000~7,000만 원"
        }
    ],
    "ISTP": [
        {
            "name": "기계설계 엔지니어",
            "major": "기계공학과",
            "personality": "실용적이고 관찰력이 뛰어나며 직접 문제를 해결하는 성향",
            "salary": "약 3,500~5,500만 원"
        },
        {
            "name": "항공정비사",
            "major": "항공정비학과, 항공기계공학과",
            "personality": "집중력이 높고 꼼꼼하며 기계를 다루는 것을 좋아하는 성향",
            "salary": "약 3,500~5,500만 원"
        }
    ],
    "ISFP": [
        {
            "name": "시각디자이너",
            "major": "시각디자인학과, 디자인학과",
            "personality": "감각적이고 창의적이며 자신만의 개성을 표현하는 성향",
            "salary": "약 3,000~4,500만 원"
        },
        {
            "name": "셰프",
            "major": "조리학과, 외식조리학과",
            "personality": "섬세하고 감각적이며 새로운 음식을 만드는 것을 좋아하는 성향",
            "salary": "약 3,000~5,000만 원"
        }
    ],
    "INFP": [
        {
            "name": "작가",
            "major": "문예창작학과, 국어국문학과",
            "personality": "상상력이 풍부하고 자신의 생각을 표현하는 성향",
            "salary": "약 2,500~4,500만 원"
        },
        {
            "name": "UX 디자이너",
            "major": "산업디자인학과, 시각디자인학과",
            "personality": "창의적이고 공감 능력이 뛰어나며 사람들의 경험을 중요하게 생각하는 성향",
            "salary": "약 3,500~5,500만 원"
        }
    ],
    "INTP": [
        {
            "name": "연구원",
            "major": "자연과학계열, 공학계열",
            "personality": "호기심이 많고 논리적으로 탐구하는 것을 좋아하는 성향",
            "salary": "약 4,000~6,000만 원"
        },
        {
            "name": "AI 개발자",
            "major": "컴퓨터공학과, 인공지능학과",
            "personality": "분석적이고 독창적이며 복잡한 문제를 해결하는 성향",
            "salary": "약 4,500~7,000만 원"
        }
    ],
    "ESTP": [
        {
            "name": "스포츠 마케터",
            "major": "스포츠산업학과, 경영학과",
            "personality": "활동적이고 순발력이 좋으며 사람들과 소통하는 성향",
            "salary": "약 3,500~5,000만 원"
        },
        {
            "name": "응급구조사",
            "major": "응급구조학과",
            "personality": "침착하고 판단력이 빠르며 책임감이 강한 성향",
            "salary": "약 3,000~4,500만 원"
        }
    ],
    "ESFP": [
        {
            "name": "호텔리어",
            "major": "호텔경영학과, 관광학과",
            "personality": "사교적이고 친절하며 사람들에게 즐거운 경험을 제공하는 성향",
            "salary": "약 3,000~4,500만 원"
        },
        {
            "name": "공연기획자",
            "major": "공연예술학과, 문화콘텐츠학과",
            "personality": "활발하고 표현력이 좋으며 사람들과 함께 일하는 성향",
            "salary": "약 3,000~4,500만 원"
        }
    ],
    "ENFP": [
        {
            "name": "광고기획자",
            "major": "광고홍보학과, 미디어학과",
            "personality": "아이디어가 풍부하고 새로운 도전을 즐기는 성향",
            "salary": "약 3,500~5,500만 원"
        },
        {
            "name": "콘텐츠 기획자",
            "major": "미디어학과, 문화콘텐츠학과",
            "personality": "창의적이고 호기심이 많으며 새로운 콘텐츠를 만드는 성향",
            "salary": "약 3,000~5,000만 원"
        }
    ],
    "ENTP": [
        {
            "name": "창업가",
            "major": "경영학과, 창업학과",
            "personality": "도전적이고 아이디어가 많으며 새로운 사업을 구상하는 성향",
            "salary": "수익에 따라 차이가 큼"
        },
        {
            "name": "변리사",
            "major": "법학과, 이공계열",
            "personality": "논리적이고 분석력이 뛰어나며 기술과 법률에 관심이 많은 성향",
            "salary": "약 5,000~9,000만 원"
        }
    ],
    "ESTJ": [
        {
            "name": "경영관리자",
            "major": "경영학과, 경제학과",
            "personality": "조직적이고 추진력이 있으며 목표를 계획적으로 달성하는 성향",
            "salary": "약 4,500~7,000만 원"
        },
        {
            "name": "공무원",
            "major": "행정학과, 법학과",
            "personality": "책임감이 강하고 규칙을 잘 지키는 성향",
            "salary": "약 3,000~4,500만 원"
        }
    ],
    "ESFJ": [
        {
            "name": "인사 담당자",
            "major": "경영학과, 행정학과",
            "personality": "친화력이 좋고 배려심이 있으며 사람들과 협력하는 성향",
            "salary": "약 3,500~5,500만 원"
        },
        {
            "name": "이벤트 기획자",
            "major": "이벤트학과, 광고홍보학과",
            "personality": "사교적이고 계획성이 있으며 다양한 행사를 준비하는 성향",
            "salary": "약 3,000~4,500만 원"
        }
    ],
    "ENFJ": [
        {
            "name": "교육 전문가",
            "major": "교육학과, 교육공학과",
            "personality": "리더십이 있고 공감 능력이 뛰어나며 다른 사람의 성장을 돕는 성향",
            "salary": "약 3,500~5,500만 원"
        },
        {
            "name": "HRD 전문가",
            "major": "교육학과, 경영학과",
            "personality": "소통 능력이 뛰어나고 사람들의 능력 개발에 관심이 많은 성향",
            "salary": "약 3,500~5,500만 원"
        }
    ],
    "ENTJ": [
        {
            "name": "경영 컨설턴트",
            "major": "경영학과, 경제학과",
            "personality": "목표 지향적이고 분석력과 리더십이 뛰어난 성향",
            "salary": "약 5,000~8,000만 원"
        },
        {
            "name": "프로덕트 매니저",
            "major": "경영학과, 컴퓨터공학과",
            "personality": "기획력과 추진력이 좋고 여러 사람과 협업하는 성향",
            "salary": "약 4,500~7,000만 원"
        }
    ]
}

# -----------------------------
# 메인 화면
# -----------------------------
st.title("🎯 MBTI 맞춤형 진로 탐색")

st.markdown(
    '<p class="subtitle">나의 성격으로 찾아보는 미래의 직업!</p>',
    unsafe_allow_html=True
)

st.write("")
st.write("🧩 **나의 MBTI를 선택해 보세요!**")

mbti = st.selectbox(
    "MBTI 유형",
    options=list(careers.keys()),
    index=None,
    placeholder="MBTI를 선택하세요"
)

# -----------------------------
# 결과 화면
# -----------------------------
if mbti is not None:

    st.divider()

    st.header("✨ " + mbti + " 추천 진로")

    st.info(
        "아래 직업은 MBTI 성향을 바탕으로 한 참고용 추천이에요. "
        "실제 진로는 개인의 흥미와 능력에 따라 달라질 수 있어요!"
    )

    col1, col2 = st.columns(2)

    for index, job in enumerate(careers[mbti]):

        if index == 0:
            current_col = col1
        else:
            current_col = col2

        with current_col:

            st.subheader(
                "💼 " + str(index + 1) + ". " + job["name"]
            )

            st.markdown("---")

            st.markdown("🎓 **추천 학과**")
            st.write(job["major"])

            st.markdown("🌟 **적합한 성격**")
            st.write(job["personality"])

            st.markdown("💰 **평균 연봉 참고 범위**")
            st.success(job["salary"])

    st.divider()

    st.subheader("🚀 나의 미래를 준비해 보자!")

    st.write(
        "관심 있는 직업을 더 자세히 조사하고 "
        "관련 학과와 필요한 능력을 알아보세요. "
        "작은 관심이 멋진 미래로 이어질 수 있어요!"
    )

    st.balloons()

else:

    st.info(
        "🌈 MBTI를 선택하면 나에게 어울리는 "
        "직업 2가지를 확인할 수 있어요!"
    )

    st.markdown("### 💡 나의 가능성을 찾아보세요!")

st.divider()

st.caption(
    "※ 연봉은 진로 탐색을 위한 대략적인 참고 범위이며 "
    "실제 통계 및 경력, 기업, 지역에 따라 달라질 수 있습니다."
)

st.caption(
    "※ MBTI는 진로를 결정하는 기준이 아닌 자기 이해를 위한 참고 자료입니다."
)
