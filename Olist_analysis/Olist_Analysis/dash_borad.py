# Can run
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


# 加載數據
merged_df = pd.read_csv(r'C:\Users\NICOLE\Desktop\VS_JDE_10\Final_PJ\Dataset\Clean csv\combined_dataset.csv')


# 數據預處理
merged_df['order_purchase_timestamp'] = pd.to_datetime(merged_df['order_purchase_timestamp'])
merged_df['order_delivered_customer_date'] = pd.to_datetime(merged_df['order_delivered_customer_date'])
merged_df['order_delivered_carrier_date'] = pd.to_datetime(merged_df['order_delivered_carrier_date'])
merged_df['order_approved_at'] = pd.to_datetime(merged_df['order_approved_at'])
merged_df['delivery_time'] = \
            (merged_df['order_delivered_customer_date'] - merged_df['order_purchase_timestamp']).dt.days
merged_df['shipping_time'] = (merged_df['order_delivered_carrier_date'] - merged_df['order_approved_at']).dt.days
merged_df['carrier_delivery_time'] = (
            merged_df['order_delivered_customer_date'] - merged_df['order_delivered_carrier_date']).dt.days
merged_df['quarter'] = merged_df['order_purchase_timestamp'].dt.to_period('Q')
merged_df['year'] = merged_df['order_purchase_timestamp'].dt.year

# 讀取並添加列名 - 各商戶評分 (seller_id & Avg_score)
seller_aspect1 = pd.read_csv(
    r'C:\Users\NICOLE\Desktop\VS_JDE_10\Final_PJ\Dataset\Clean csv\商戶維度\各商戶評分(seller_id & Avg_score).csv',
    header=None)
seller_aspect1.columns = ['seller_id', 'avg_score']

# 讀取並添加列名 - 各州商戶數量分佈 (OK)
seller_aspect2 = pd.read_csv(
    r'C:\Users\NICOLE\Desktop\VS_JDE_10\Final_PJ\Dataset\Clean csv\商戶維度\各州商戶數量分佈 (OK).csv', header=None)
seller_aspect2.columns = ['state', 'seller_count']

# 讀取並添加列名 - 商戶不同售額分佈 (商戶總售額 & 商戶數量)
seller_aspect3 = pd.read_csv(
    r'C:\Users\NICOLE\Desktop\VS_JDE_10\Final_PJ\Dataset\Clean csv\商戶維度\商戶不同售額分佈(商戶總售額&商戶數量).csv',
    header=None)
seller_aspect3.columns = ['total_sales', 'seller_count']

# 讀取 - 商戶訂單數量範圍
seller_aspect4 = pd.read_csv(
    r'C:\Users\NICOLE\Desktop\VS_JDE_10\Final_PJ\Dataset\Clean csv\商戶維度\商戶訂單數量範圍.csv')
seller_aspect4.columns = ['seller_id', 'order_count', 'order_count_range']

# 讀取 - 各商戶售額_分类(最低1, 最高5)
seller_aspect5 = pd.read_csv(
    r'C:\Users\NICOLE\Desktop\VS_JDE_10\Final_PJ\Dataset\Clean csv\商戶維度\各商戶售額_分类(最低1, 最高5).csv')
seller_aspect5.columns = ['seller_record_id', 'seller_id', 'sale_volume', 'level']

# 初始化 Dash 應用
app = dash.Dash(__name__)

# 定義佈局
app.layout = html.Div([
    html.H1("Olist's E-commerce Dashboard"),
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': '2016-2018', 'value': 'all'}] + [{'label': str(year), 'value': year} for year in
                                                                sorted(merged_df['year'].unique())],
            value='all',
            style={'width': '200px'}
        ),
    ], style={'margin-bottom': '20px'}),
    dcc.Tabs([
        dcc.Tab(label='商戶維度分析', children=[
            dcc.Graph(id='Seller-Distribution-by-State'),
            dcc.Graph(id='Seller-Sales-Distribution'),
            dcc.Graph(id='Seller-Ratings'),
            dcc.Graph(id='Seller-Order-Quantity-Range'),
            dcc.Graph(id='Seller-Sales-Categories')
        ]),
        dcc.Tab(label='產品維度分析', children=[
            dcc.Graph(id='Sales-Trend-by-Top-7-Categories'),
            dcc.Graph(id='Product-Clustering-Analysis')
        ]),
        dcc.Tab(label='交付情況分析(種類)', children=[
            dcc.Graph(id='Top-10-Categories-by-Cancellation-Rate'),
            dcc.Graph(id='Shipping-Time-by-Top-10-Categories'),
            dcc.Graph(id='Carrier-Delivery-Time-by-Top-10-Categories'),
            dcc.Graph(id='Delivery-Delay-Distribution')
        ]),
        dcc.Tab(label='交付情況分析(地區)', children=[
            dcc.Graph(id='Delivery-Time-by-Region'),
            dcc.Graph(id='Order-Status-Distribution'),
            dcc.Graph(id='Order-Status-Over-Time'),
            dcc.Graph(id='Cancellation-Rate-by-State'),
            dcc.Graph(id='Payment-Type-Distribution')
        ]),
    ]),
])


# 回調函數
@app.callback(
    [Output('Sales-Trend-by-Top-7-Categories', 'figure'),
     Output('Top-10-Categories-by-Cancellation-Rate', 'figure'),
     Output('Shipping-Time-by-Top-10-Categories', 'figure'),
     Output('Carrier-Delivery-Time-by-Top-10-Categories', 'figure'),
     Output('Delivery-Delay-Distribution', 'figure'),
     Output('Delivery-Time-by-Region', 'figure'),
     Output('Order-Status-Distribution', 'figure'),
     Output('Order-Status-Over-Time', 'figure'),
     Output('Cancellation-Rate-by-State', 'figure'),
     Output('Payment-Type-Distribution', 'figure'),
     Output('Product-Clustering-Analysis', 'figure'),
     Output('Seller-Distribution-by-State', 'figure'),
     Output('Seller-Sales-Distribution', 'figure'),
     Output('Seller-Ratings', 'figure'),
     Output('Seller-Order-Quantity-Range', 'figure'),
     Output('Seller-Sales-Categories', 'figure')],
    Input('year-dropdown', 'value')
)
def update_graphs(selected_year):
    if selected_year == 'all':
        filtered_df = merged_df.copy()
        year_label = '2016-2018'
    else:
        filtered_df = merged_df[merged_df['year'] == selected_year].copy()
        year_label = str(selected_year)

    # 創建一個顏色映射
    top7_categories = filtered_df.groupby('product_category_name_english')['price'].sum().nlargest(7).index
    color_map = px.colors.qualitative.Plotly  # 使用Plotly的默認顏色方案
    category_color_map = {category: color_map[i % len(color_map)] for i, category in enumerate(top7_categories)}

    # Sales Trend by Top 7 Categories
    category_sales = filtered_df.groupby(['product_category_name_english', 'quarter'])['price'].sum().reset_index()
    fig1 = go.Figure()
    for category in top7_categories:
        category_data = category_sales[category_sales['product_category_name_english'] == category]
        category_trend = category_data.groupby('quarter')['price'].sum()
        fig1.add_trace(go.Scatter(
            x=category_trend.index.astype(str),
            y=category_trend.values,
            mode='lines+markers',
            name=category,
            line=dict(color=category_color_map[category])
        ))
    fig1.update_layout(
        title=f'Sales Trend by Top 7 Categories ({year_label})',
        xaxis_title='Quarter',
        yaxis_title='Total Sales Volume',
        legend_title='Category'
    )

    # Top 10 Categories by Cancellation Rate
    category_cancellation_rate = (filtered_df[filtered_df['order_status'] == 'canceled'].groupby(
        'product_category_name_english').size() / filtered_df.groupby('product_category_name_english').size()) * 100
    fig2 = px.bar(x=category_cancellation_rate.nlargest(10).index, y=category_cancellation_rate.nlargest(10).values,
                  title=f'Top 10 Categories by Cancellation Rate ({year_label})',
                  labels={'x': 'Product Category', 'y': 'Cancellation Rate (%)'},
                  color=category_cancellation_rate.nlargest(10).values,
                  color_continuous_scale=px.colors.sequential.Viridis)
    fig2.update_layout(xaxis_tickangle=-45, coloraxis_showscale=False)

    # Shipping Time by Top 10 Categories
    positive_shipping_time = filtered_df[filtered_df['shipping_time'] >= 0]
    top10_shipping_time = positive_shipping_time.groupby('product_category_name_english')[
        'shipping_time'].mean().nlargest(10)
    fig3 = px.box(
        positive_shipping_time[positive_shipping_time['product_category_name_english'].isin(top10_shipping_time.index)],
        x='product_category_name_english', y='shipping_time',
        title=f'Shipping Time by Top 10 Categories ({year_label})',
        labels={'product_category_name_english': 'Product Category', 'shipping_time': 'Shipping Time (days)'},
        color='product_category_name_english',
        category_orders={'product_category_name_english': top10_shipping_time.index})
    fig3.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': top10_shipping_time.index})

    # Carrier Delivery Time by Top 10 Categories
    top10_carrier_delivery_time = filtered_df.groupby('product_category_name_english')[
        'carrier_delivery_time'].mean().nlargest(10)
    fig4 = px.box(filtered_df[(filtered_df['product_category_name_english'].isin(top10_carrier_delivery_time.index)) & (
                filtered_df['carrier_delivery_time'] >= 0)], x='product_category_name_english',
                  y='carrier_delivery_time', title=f'Carrier Delivery Time by Top 10 Categories ({year_label})',
                  labels={'product_category_name_english': 'Product Category',
                          'carrier_delivery_time': 'Carrier Delivery Time (days)'},
                  color='product_category_name_english',
                  category_orders={'product_category_name_english': top10_carrier_delivery_time.index})
    fig4.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': top10_carrier_delivery_time.index})

    # Delivery Delay Distribution
    delivered_orders = filtered_df[filtered_df['order_status'] == 'delivered']
    delivered_orders['delay'] = (delivered_orders['order_delivered_customer_date'] -
                                 pd.to_datetime(delivered_orders['order_estimated_delivery_date'])).dt.days
    fig5 = px.histogram(delivered_orders[delivered_orders['delay'] >= 0], x='delay',
                        title=f'Delivery Delay Distribution ({year_label})',
                        labels={'delay': 'Delay (days)', 'count': 'Count'},
                        color_discrete_sequence=['#FF4136'])
    delay_proportion = (delivered_orders['delay'] > 0).mean()
    fig5.add_vline(x=0, line_dash="dash", line_color="red",
                   annotation_text=f"Expected Delivery Date (Delay Proportion: {delay_proportion:.2%})")

    max_count = delivered_orders['delay'].value_counts().max()
    y_max = 2000 if max_count > 1000 else max_count + 1000
    fig5.update_layout(yaxis_range=[0, y_max], xaxis_range=[0, 50])

    over_50_days = delivered_orders[delivered_orders['delay'] > 50]['delay']
    max_delay = int(over_50_days.max())
    bins = list(range(51, max_delay + 10, 10))
    over_50_days_counts = pd.cut(over_50_days, bins=bins).value_counts().sort_index()
    over_50_days_text = '<br>'.join(
        [f"{int(b.left)}-{int(b.right)} days: {count} cases" for b, count in over_50_days_counts.items()])

    fig5.add_annotation(
        x=1.05, y=0.95, xref='paper', yref='paper',
        text=f"Cases over 50 days:<br>{over_50_days_text}",
        showarrow=False, align='left',
        bgcolor='rgba(255,255,255,0.8)', bordercolor='black', borderwidth=1
    )

    # Delivery Time by Region
    top10_delivery_time = filtered_df.groupby('customer_state')['delivery_time'].mean().nlargest(10)
    fig6 = px.box(filtered_df[filtered_df['customer_state'].isin(top10_delivery_time.index)], x='customer_state',
                  y='delivery_time', title=f'Delivery Time by Top 10 Regions ({year_label})',
                  labels={'customer_state': 'Customer State', 'delivery_time': 'Delivery Time (days)'},
                  color='customer_state', category_orders={'customer_state': top10_delivery_time.index})
    fig6.update_layout(xaxis={'categoryorder': 'array', 'categoryarray': top10_delivery_time.index})

    # Order Status Distribution
    order_status_dist = filtered_df['order_status'].value_counts(normalize=True) * 100
    other_threshold = 5
    small_categories = order_status_dist[order_status_dist < other_threshold].index
    order_status_dist_copy = order_status_dist.copy()
    order_status_dist_copy.loc['other'] = order_status_dist[small_categories].sum()
    order_status_dist_copy = order_status_dist_copy[~order_status_dist_copy.index.isin(small_categories)]

    colors = px.colors.qualitative.Bold
    colors[-1] = '#AAAAAA'  # Set 'other' category to gray

    fig7 = go.Figure(data=[go.Pie(labels=order_status_dist_copy.index, values=order_status_dist_copy.values,
                                  textposition='outside', textinfo='label+percent',
                                  marker=dict(colors=colors, line=dict(color='#000000', width=1.5)))])
    fig7.update_layout(title=f'Order Status Distribution ({year_label})')

    other_details = filtered_df[filtered_df['order_status'].isin(small_categories)]
    other_details_dist = other_details['order_status'].value_counts(normalize=True) * 100
    other_details_text = '<br>'.join(
        [f"{status}: {percentage:.2f}%" for status, percentage in other_details_dist.items()])

    fig7.add_annotation(
        text=f"Other includes:<br>{other_details_text}",
        x=-0.2, y=0.5,
        showarrow=False,
        xref="paper", yref="paper",
        align='left',
        font=dict(size=18)
    )

    # Order Status Over Time
    status_over_time = filtered_df.groupby(
        [filtered_df['order_purchase_timestamp'].dt.to_period('M'), 'order_status']).size().unstack(fill_value=0)

    fig8 = go.Figure()

    # 添加除了 'delivered' 狀態的其他狀態的面積圖
    for status in status_over_time.columns:
        if status != 'delivered':
            fig8.add_trace(go.Scatter(
                x=status_over_time.index.astype(str),
                y=status_over_time[status],
                mode='lines',  # 使用線條模式
                stackgroup='one',  # 堆疊到同一組
                name=status
            ))

    fig8.update_layout(
        title=f'Order Status Over Time ({year_label})',
        xaxis_title='Month',
        yaxis_title='Count',
        legend_title='Order Status'
    )

    fig8.show()

    # Cancellation Rate by State
    state_cancellation_rate = (filtered_df[filtered_df['order_status'] == 'canceled'].groupby('customer_state').size() /
                               filtered_df.groupby('customer_state').size()) * 100

    fig9 = make_subplots(rows=1, cols=2,
                         specs=[[{'type': 'xy'}, {'type': 'domain'}]],
                         column_widths=[0.7, 0.3],
                         subplot_titles=(f'Cancellation Rate by State ({year_label})',
                                         'Top State City Distribution'))

    # 添加熱力圖
    heatmap = go.Heatmap(
        z=state_cancellation_rate.values.reshape(1, -1),
        x=state_cancellation_rate.index,
        y=['Cancellation Rate'],
        colorscale='Reds',
        showscale=True,
        colorbar=dict(title='Cancellation Rate (%)', x=-0.15, thickness=20)
    )
    fig9.add_trace(heatmap, row=1, col=1)

    # 更新佈局以縮短 y 軸
    fig9.update_layout(
        height=400,  # 減小整體高度
        yaxis=dict(
            tickvals=[],  # 移除 y 軸刻度
            ticktext=[],  # 移除 y 軸標籤
            showticklabels=False,  # 隱藏 y 軸標籤
            fixedrange=True  # 固定 y 軸範圍
        ),
        xaxis=dict(
            tickangle=-45,  # 旋轉 x 軸標籤
            automargin=True  # 自動調整邊距以適應標籤
        )
    )

    # 更新佈局，為底部文本留出空間
    fig9.update_layout(
        height=500,  # 增加圖表高度
        margin=dict(b=0)  # 增加底部邊距
    )

    # 創建城市列表文本
    city_text = ""
    for state in state_cancellation_rate.index:
        cities = filtered_df[filtered_df['customer_state'] == state]['customer_city'].unique()
        city_list = ', '.join(cities[:5])  # 只顯示前5個城市
        city_text += f"{state}: {city_list}<br>"

    # 添加城市列表註釋
    fig9.add_annotation(
        xref='paper',
        yref='paper',
        x=2,
        y=-5,  # 將文本放在圖表where
        text=city_text,
        showarrow=False,
        align='left',
        font=dict(size=15),
        bordercolor='black',
        borderwidth=0.8,
        bgcolor='white',
        opacity=0.8
    )

    # 找出取消率最高的州
    top_state = state_cancellation_rate.idxmax()
    top_state_cities = filtered_df[filtered_df['customer_state'] == top_state]['customer_city'].value_counts()

    # 添加餅圖
    pie = go.Pie(
        labels=top_state_cities.index[:10],  # Top 10 cities
        values=top_state_cities.values[:10],
        textinfo='label+percent',
        hole=0.3,
        domain=dict(x=[0.6, 0.95], y=[0.2, 0.8])  # 縮小餅圖
    )
    fig9.add_trace(pie, row=1, col=2)

    # 添加餅圖的說明
    fig9.add_annotation(
        text="<br>".join(top_state_cities.index[:10].tolist()),
        xref="paper", yref="paper",
        x=-2, y=3,
        showarrow=False,
        align="left",
        font=dict(size=8)
    )

    # Payment Type Distribution
    payment_type_dist = filtered_df['payment_type'].value_counts(normalize=True) * 100
    fig10 = px.treemap(
        data_frame=pd.DataFrame({'payment_type': payment_type_dist.index, 'value': payment_type_dist.values}),
        path=['payment_type'],
        values='value',
        title=f'Payment Type Distribution ({year_label})',
        labels={'value': '百分比'}
    )
    fig10.update_traces(textinfo='label+value+percent parent',
                        textfont=dict(size=14, family="Arial Black"))
    fig10.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        title_font=dict(size=24, family="Arial Black"),
        font=dict(size=14, family="Arial Black")
    )

    # Product Clustering Analysis
    product_cluster = filtered_df.groupby('product_category_name_english').agg({
        'payment_value': 'sum',
        'review_score': 'mean'
    }).reset_index()
    fig11 = px.scatter(
        product_cluster,
        x='payment_value',
        y='review_score',
        color='product_category_name_english',
        hover_name='product_category_name_english',
        size='payment_value',
        size_max=80,
        title=f'產品聚類分析 - 銷量及評分 ({year_label})',
        labels={
            'payment_value': '總銷售額',
            'review_score': '平均評分',
            'product_category_name_english': '產品類別'
        },
        color_discrete_map=category_color_map  # 使用相同的顏色映射
    )

    fig11.update_traces(
        text=product_cluster['payment_value'].apply(lambda x: f'總銷售額: {x:.0f}'),
        textposition='top center'
    )
    fig11.update_layout(
        height=800,
        legend_title_text='產品類別',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.75,
            xanchor="right",
            x=1
        ),
        xaxis=dict(
            title='總銷售額',
            tickangle=0,
            title_standoff=10,
            tickformat=',d'
        )
    )
    fig11.add_annotation(
        xanchor="center",
        yanchor="top",
        y=0.5,
        xref="paper",
        yref="paper",
        text="總銷售額",
        showarrow=False,
        textangle=0,
        font=dict(size=12)
    )
    fig11.update_xaxes(title=None)

    # 商戶分佈圖
    fig12 = px.bar(seller_aspect2, x='state', y='seller_count', title='各州商戶數量分佈',
                   color_discrete_sequence=['#FF9999'])  # 使用淺紅色

    # 商戶銷售額分佈圖
    fig13 = px.bar(seller_aspect3, x='total_sales', y='seller_count', title='商戶銷售額分佈',
                   color_discrete_sequence=['#66B2FF'])  # 使用淺藍色

    # 商戶評分分佈圖
    fig14 = px.histogram(seller_aspect1, x='avg_score', title='商戶評分分佈',
                         color_discrete_sequence=['#99FF99'])  # 使用淺綠色

    # 商戶訂單數量範圍圖（改為餅圖）
    fig15 = px.pie(seller_aspect4,
                   names='order_count_range',
                   values='order_count',
                   title='商戶訂單數量範圍分佈',
                   hover_data=['order_count'])

    # 添加百分比顯示，將標籤移到餅圖外部
    fig15.update_traces(textposition='outside', textinfo='percent+label')

    # 在圖表右側添加數字範圍作為文本
    fig15.add_annotation(
        x=1.1, y=-2, xref='paper', yref='paper',
        text="訂單數量範圍:\n" + "\n".join(seller_aspect4['order_count_range'].unique()),
        showarrow=False, align='left',
        font=dict(size=15),
        bordercolor='black', borderwidth=1, bgcolor='white', opacity=0.8
    )

    # 首先，計算每個等級的最小和最大銷售額
    level_stats = seller_aspect5.groupby('level').agg({'sale_volume': ['min', 'max']})
    level_stats.columns = ['min_sale', 'max_sale']

    # 創建一個字典來映射等級到描述，包括銷售額範圍
    level_labels = {
        1: f'1等級-最低 (${level_stats.loc[1, "min_sale"]:.0f} - ${level_stats.loc[1, "max_sale"]:.0f})',
        2: f'2等級 (${level_stats.loc[2, "min_sale"]:.0f} - ${level_stats.loc[2, "max_sale"]:.0f})',
        3: f'3等級 (${level_stats.loc[3, "min_sale"]:.0f} - ${level_stats.loc[3, "max_sale"]:.0f})',
        4: f'4等級-最高 (${level_stats.loc[4, "min_sale"]:.0f} - ${level_stats.loc[4, "max_sale"]:.0f})'
    }

    # 創建餅圖
    fig16 = px.pie(
        seller_aspect5,
        names='level',
        values='sale_volume',
        title='商戶銷售額類別分佈',
        labels={'level': '銷售額等級', 'sale_volume': '總銷售額'}
    )

    # 更新標籤，將標籤移到餅圖外部
    fig16.update_traces(
        text=[level_labels[level] for level in seller_aspect5['level']],
        textposition='outside'
    )

    # 調整布局
    fig16.update_layout(
        legend_title_text='銷售額等級',
        uniformtext_minsize=15,
        uniformtext_mode='hide'
    )

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, fig11, fig12, fig13, fig14, fig15, fig16


# Run the application
if __name__ == '__main__':
    app.run_server(debug=False, host='192.168.0.219', port=8502)

