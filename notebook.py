import marimo

__generated_with = "0.14.12"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""# Yale School by Gender""")
    return


@app.cell
def _():
    # TODO
    # add Total University
    # fix tooltips
    import marimo as mo
    import polars as pl
    import altair as alt
    return alt, mo, pl


@app.cell
def _(mo, pl):
    dataLoc = mo.notebook_location() / "public" / "w010-yale-school-gender.csv"
    df = pl.read_csv(str(dataLoc))
    longDat = df.unpivot(index = ["Year", "School"], variable_name="Gender", value_name="Count")
    longDat = longDat.fill_null('0').with_columns(pl.col('Count').cast(pl.UInt64))
    gender_enum = pl.Enum(["M","W","N or Unknown"])
    longDat = longDat.with_columns(pl.col("Gender").cast(gender_enum))
    return (longDat,)


@app.cell
def _(longDat):
    yrs = longDat.get_column("Year").unique().sort(descending=True).to_list()
    return (yrs,)


@app.cell
def _(mo, yrs):
    y = mo.ui.dropdown(options=yrs, value=2024)
    y
    return (y,)


@app.cell
def _(longDat, pl, y):
    yrDat = longDat.filter(pl.col('Year') == y.value)
    return


@app.cell
def _(alt, longDat, mo, y):
    gender_order = ["M","W","N or Unknown"]

    yrChart = mo.ui.altair_chart(
        alt.Chart(longDat).mark_bar().encode(
            x=alt.X('sum(Count)', stack='normalize', title=''),
            y=alt.Y('School:N', title=''),
            color=alt.Color(
                'Gender:N',
                scale=alt.Scale(range=['#00356B','#63aaff','#286dc0']),
                sort=gender_order                 
            ),
            order='order:O'
        ).properties(title=f'Gender Percentages by School, {y.value}')
    )

    yrChart
    return


@app.cell
def _(longDat):
    opts = longDat.get_column("School").unique().to_list()
    return (opts,)


@app.cell
def _(mo, opts):
    x = mo.ui.dropdown(options=opts, value="Yale College")
    x
    return (x,)


@app.cell
def _(longDat, pl, x):
    selectedDat = longDat.filter(pl.col('School') == x.value)
    return (selectedDat,)


@app.cell
def _(alt, mo, selectedDat, x):
    chart = mo.ui.altair_chart(alt.Chart(selectedDat).mark_bar().encode(
        x=alt.X('Year:O').title(''),
        y=alt.Y('Count:Q').title(''),
        color = alt.Color('Gender', 
                          scale = alt.Scale(range=['#00356B','#63aaff','#286dc0'])),
        order='order:O'
    ).properties(title=f'Gender Headcounts: {x.value}'))

    chart
    return


if __name__ == "__main__":
    app.run()
