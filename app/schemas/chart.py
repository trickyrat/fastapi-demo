from typing import Optional, Any

from pydantic import BaseModel


class BackgroundStyle(BaseModel):
    color: Optional[str]


class Series(BaseModel):
    name: Optional[str]
    data: list[int]
    type: str
    showBackground: bool = False
    backgroundStyle: Optional[BackgroundStyle]
    stack: Optional[str]


class BarSeries(Series):
    type = 'bar'


class LineSeries(Series):
    type = 'line'


class Legend(BaseModel):
    data: list[str]


class ChartTitle(BaseModel):
    text: Optional[str]
    link: Optional[str]
    left: Optional[str]
    right: Optional[str]
    top: Optional[str]
    bottom: Optional[str]


class AxisLabel(BaseModel):
    interval: Optional[int | str] = "auto"
    show: bool = True
    margin: Optional[int] = 8
    rotate: Optional[int] = 0
    inside: Optional[bool] = False


class Axis(BaseModel):
    type: str
    data: Optional[list[str]]
    show: bool = True
    axisLabel: Optional[AxisLabel]


class ChartTooltip(BaseModel):
    trigger: Optional[str]


class ToolboxFeature(BaseModel):
    saveAsImage: Any


class Toolbox(BaseModel):
    feature: Optional[ToolboxFeature]


class ChartGrid(BaseModel):
    left: Optional[str]
    right: Optional[str]
    bottom: Optional[str]
    containLabel: bool | None


class Chart(BaseModel):
    title: Optional[ChartTitle]
    xAxis: Axis
    series: list[Series]
    legend: Optional[Legend]
    yAxis: Axis
    tooltip: Optional[ChartTooltip]
    grid: Optional[ChartGrid]
